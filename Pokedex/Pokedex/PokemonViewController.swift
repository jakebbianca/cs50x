import UIKit

class PokemonViewController: UIViewController {
    
    var url: String!
    var caught: Bool = false

    @IBOutlet var nameLabel: UILabel!
    @IBOutlet var numberLabel: UILabel!
    @IBOutlet var type1Label: UILabel!
    @IBOutlet var type2Label: UILabel!
    @IBOutlet var catchButton: UIButton!
    @IBOutlet var image: UIImageView!
    @IBOutlet var flavor: UILabel!
    
    
    func capitalize(text: String) -> String {
        return text.prefix(1).uppercased() + text.dropFirst()
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)

        nameLabel.text = ""
        numberLabel.text = ""
        type1Label.text = ""
        type2Label.text = ""
        flavor.text = ""

        loadPokemon()
    }


    func loadPokemon() {
        URLSession.shared.dataTask(with: URL(string: url)!) { (data, response, error) in
            guard let data = data else {
                return
            }

            do {
                let result = try JSONDecoder().decode(PokemonResult.self, from: data)
                
                // Get image for each Pokemon
                guard let imageURL = URL(string: result.sprites.front_default!) else {
                    return
                }
                let urlData = try Data(contentsOf: imageURL)
                
                DispatchQueue.main.async {
                    self.navigationItem.title = self.capitalize(text: result.name)
                    self.nameLabel.text = self.capitalize(text: result.name)
                    self.numberLabel.text = String(format: "#%03d", result.id)
                    if UserDefaults.standard.bool(forKey: self.nameLabel.text!) {
                        self.caught = true
                        self.catchButton.setTitle("Release", for: [])
                        self.catchButton.setTitleColor(.red, for: [])
                    }
                    else {
                        self.caught = false
                        self.catchButton.setTitle("Catch", for: [])
                        self.catchButton.setTitleColor(.blue, for: [])
                    }

                    for typeEntry in result.types {
                        if typeEntry.slot == 1 {
                            self.type1Label.text = typeEntry.type.name
                        }
                        else if typeEntry.slot == 2 {
                            self.type2Label.text = typeEntry.type.name
                        }
                    }
                    
                    // Finally load image of selected pokemon
                    self.image.image = UIImage(data: urlData)
                }
                
                // Call API for species URL
                URLSession.shared.dataTask(with: URL(string: result.species.url)!) { (speciesData, speciesResponse, speciesError) in
                    guard let speciesData = speciesData else {
                        return
                    }
                    
                    do {
                        let speciesResult = try JSONDecoder().decode(PokemonSpeciesResult.self, from: speciesData)
                        
                        DispatchQueue.main.async {
                            for text in speciesResult.flavor_text_entries {
                                if text.language.name == "en" {
                                    self.flavor.text = text.flavor_text.replacingOccurrences(of: "\n", with: " ")
                                }
                            }
                        }
                    }
                    catch let speciesError {
                        print(speciesError)
                    }
                }.resume()
            }
            catch let error {
                print(error)
            }
        }.resume()
    }
    
    // Usage of [] is shorthand here for .normal
    // We are saying that these cases are for normal UIState(s)
    @IBAction func toggleCatch() {
        caught = !caught
        UserDefaults.standard.set(caught, forKey: nameLabel.text!)
        if UserDefaults.standard.bool(forKey: nameLabel.text!) {
            catchButton.setTitle("Release", for: [])
            catchButton.setTitleColor(.red, for: [])
        }
        else {
            catchButton.setTitle("Catch", for: [])
            catchButton.setTitleColor(.blue, for: [])
        }
    }
}
