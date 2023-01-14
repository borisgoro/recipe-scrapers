# mypy: allow-untyped-defs

from ._abstract import AbstractScraper


class RutgerBakt(AbstractScraper):
    @classmethod
    def host(cls):
        return "rutgerbakt.nl"

    def author(self):
        return "Rutger van den Broek"

    def title(self):
        return self.schema.title().replace(" – recept", "").replace(" – Recept","")

    def category(self):
        category = self.url.split("rutgerbakt.nl/")[-1].split("/")[0].replace("-recepten", "").replace("-", " ")
        return category

    def total_time(self):
        return self.schema.total_time()

    def yields(self):
        # The yields are all over the place. There is no way to parse this.
        return None

    def image(self):
        return self.schema.image()

    def ingredients(self):
        return self.schema.ingredients()

    def instructions(self):
        # Find the "instructions" heading It is not really clear when that is. So several steps need to be taken.
        
        # 1. Filter all the headings.
        # Some h2 headers contain photos. Those are not what we want.
        def filterHeading(headings_old):
            headings_new = []
            for heading in headings_old:
                if "class" in heading.attrs:
                    if any("photo" in attr.lower() for attr in heading.attrs["class"]):
                        continue
                headings_new.append(heading)
            return headings_new

        headings = filterHeading(self.soup.find_all("h2"))

        # 2. Find the instructions heading
        # Usually the last heading are the instructions (therefore headings.reverse()). 
        # But it's double checked whether the heading contains any of the key words.
        # I split the heading into words so I keep word boundaries in check.
        headings.reverse()
        for heading in headings:
            keyword_found=False
            for keyword in ["recept", "bereiding", "maken", "maak"]:
                if keyword in heading.getText().lower().split(" "):
                    keyword_found=True
                    break
            if keyword_found:
                break 
    
        # This function iterates over every next element after the heading.
        def parseInstructions(element, instructions):
            try:
                instruction = element.find_next_sibling()
                if instruction.name in ["p", "h2", "h3", "h4"]:
                    if not any(item in instruction.text.lower() for item in ["foto: ", "foto's: ", "foto’s: "]):
                        instructions.append(instruction.text.replace("\n", " ").strip())
                    return parseInstructions(instruction, instructions)

                else: 
                    return instructions
            except AttributeError:
                return instructions

        instructions = parseInstructions(heading, [])
        return "\n".join(instructions)


    def ratings(self):
        return self.schema.ratings()

    def description(self):
        # assuming the first paragraph is the description.
        return self.soup.find("p").text.replace("\n"," ")
