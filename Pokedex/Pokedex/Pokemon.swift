import Foundation

struct PokemonListResults: Codable {
    let results: [PokemonListResult]
}

struct PokemonListResult: Codable {
    let name: String
    let url: String
}

struct PokemonResult: Codable {
    let id: Int
    let name: String
    let types: [PokemonTypeEntry]
    let sprites: PokemonSpriteEntry
    let species: PokemonSpecies
}

struct PokemonTypeEntry: Codable {
    let slot: Int
    let type: PokemonType
}

struct PokemonType: Codable {
    let name: String
}

struct PokemonSpriteEntry: Codable {
    let back_default: String?
    let back_female: String?
    let back_shiny: String?
    let back_shiny_female: String?
    let front_default: String?
    let front_female: String?
    let front_shiny: String?
    let front_shiny_female: String?
}

// Structs below to be used for pulling description/flavor text for selected pokemon
struct PokemonSpecies: Codable {
    let name: String
    let url: String
}

struct PokemonSpeciesResult: Codable {
    let flavor_text_entries: [FlavorEntry]
}

struct FlavorEntry: Codable {
    let flavor_text: String
    let language: FlavorLanguageResult
    let version: FlavorVersionResult
}

struct FlavorLanguageResult: Codable {
    let name: String
    let url: String
}

struct FlavorVersionResult: Codable {
    let name: String
    let url: String
}
