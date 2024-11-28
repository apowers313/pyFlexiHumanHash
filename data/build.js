const fs = require("node:fs");
const path = require("node:path");
const fetch = require("node-fetch");

function build(name, words) {
    filepath = path.resolve("build", name)
    fs.writeFileSync(filepath, words.join("\n"))
}

build("noun", require("categorized-words").N)
build("adjective", require("categorized-words").A)
build("verb", require("categorized-words").V)
build("city", require("all-the-cities").map((c) => c.name))
build("female-name", require("@stdlib/datasets-female-first-names-en")())
build("male-name", require("@stdlib/datasets-male-first-names-en")())
build("first-name", require("@stdlib/datasets-female-first-names-en")().concat(require("@stdlib/datasets-male-first-names-en")()))

fetch("https://raw.githubusercontent.com/Debdut/uuid-readable/refs/heads/master/data/name/last.json")
    .then(res => res.json())
    .then((json) => {
        build("last-name", json)
    });