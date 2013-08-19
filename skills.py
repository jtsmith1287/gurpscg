

A = "weapon combat melee"
B = "weapon combat ranged"
C = "hand combat"
D = "crafting"
E = "every man"
M = "medicine"
T = "tech"
O = "occult"
S = "social"
G = "magic"

SKILLS = [
          ["Name", "Attribute", "Difficulty", "TL", "Page", "Category"],
          ["Axe/Mace", "DX", "A",  1, "208", [A]],
          ["Garrote", "DX", "E",  3, "208", [C]],
          ["Carpentry", "IQ", "E",  0, "208", [D]],
          ["Boxing", "DX", "A", 0, "182", [C]],
          ["Brawling", "DX", "E",  0, "182", [C]],
          ["Broadsword", "DX", "A",  0, "208", [A]],
          ["Cloak", "DX", "A",  0, "184", [A, C]],
          ["Fast-Draw", "DX", "E",  0, "194", [A, B]],
          ["Flail", "DX", "H",  0, "208", [A]],
          ["Force Sword", "DX", "A",  0, "208", [A]],
          ["Force Whip", "DX", "A",  0, "209", [A]],
          ["Jitte/Sai", "DX", "A",  0, "208", [A]],
          ["Judo", "DX", "H",  0, "203", [C]],
          ["Karate", "DX", "H",  0, "203", [C]],
          ["Knife", "DX", "E",  0, "208", [A]],
          ["Kusari", "DX", "H",  0, "209", [A]],
          ["Lance", "DX", "A",  0, "204", [A]],
          ["Main-Gauche", "DX", "A",  0, "208", [A]],
          ["Monowire Whip", "DX", "H",  0, "209", [A]],
          ["Parry Missile Weapons", "DX", "H",  0, "212", [A]],
          ["Polearm", "DX", "A",  0, "208", [A]],
          ["Rapier", "DX", "A",  0, "208", [A]],
          ["Saber", "DX", "A",  0, "208", [A]],
          ["Shield", "DX", "E",  0, "220", [A]],
          ["Shortsword", "DX", "A",  0, "209", [A]],
          ["Smallsword", "DX", "A",  0, "208", [A]],
          ["Spear", "DX", "A",  0, "208", [A]],
          ["Staff", "DX", "A",  0, "208", [A]],
          ["Sumo Wrestling", "DX", "A",  0, "223", [C]],
          ["Tonfa", "DX", "A",  0, "209", [A]],
          ["Two-Handed Axe/Mace", "DX", "A",  0, "208", [A]],
          ["Two-Handed Flail", "DX", "H",  0, "208", [A]],
          ["Two-Handed Sword", "DX", "A",  0, "209", [A]],
          ["Whip", "DX", "A",  0, "209", [A]],
          ["Wrestling", "DX", "A",  0, "228", [C]],
          ["Area Knowledge", "IQ", "E", 0, "176", [E]],
          ["Computer Operation/TL", "IQ", "E", 0, "184", [E, T]],
          ["Cooking", "IQ", "A", 0, "185", [E, D]],
          ["Current Affairs/TL", "IQ", "E", 0, "186", [S,E]],
          ["First Aid/TL", "IQ", "E", 0, "195", [E]],
          ["Housekeeping", "IQ", "E", 0, "200", [E]],
          ["Knot-Tying", "DX", "E", 0, "203", [E,D]],
          ["Savoir-Faire", "IQ", "E", 0, "218", [S, E]],
          ["Sewing/TL", "DX", "E", 0, "219", [D, E]],
          ["Typing", "DX", "E", 0, "228", [T, E]],
          ["Weather Sense", "IQ", "A", 0, "209", [E]],
          ["Diagnosis/TL", "IQ", "H", 0, "187", [M]],
          ["Electronics Operation/TL (Medical)", "IQ", "A", 0, "189", [T, M]],
          ["Esoteric Medicine", "Per", "H", 0, "192", [M]],
          ["Expert Skill (Epidemiology)", "IQ", "H", 0, "193", [M]],
          ["First Aid/TL", "IQ", "E", 0, "195", [M]],
          ["Hypnotism", "IQ", "H", 0, "201", [O, M]],
          ["Pharmacy/TL", "IQ", "H", 0, "213", [M]],
          ["Physician/TL", "IQ", "H", 0, "213", [M]],
          ["Physiology/TL", "IQ", "H", 0, "213", [M]],
          ["Poisons/TL", "IQ", "H", 0, "214", [M,D,O]],
          ["Psychology", "IQ", "H", 0, "216", [M,O]],
          ["Surgery/TL", "IQ", "VH", 0, "223", [M,O]],
          ["Veterinary/TL", "IQ", "H", 0, "228", [M]],
          ["Alchemy/TL", "IQ", "VH", 0, "174", [D,G,M,O]],
          ["Exorcism", "Will", "H", 0, "193", [O, M]],
          ["Expert Skill (Psionics)", "IQ", "H", 0, "193", [G]],
          ["Herb Lore/TL", "IQ", "VH", 0, "199", [O]],
          ["Hidden Lore (Demon Lore)", "IQ", "A", 0, "199", [O]],
          ["Hidden Lore (Faerie Lore)", "IQ", "A", 0, "199", [O]],
          ["Hidden Lore (Spirit Lore)", "IQ", "A", 0, "199", [O]],
          ["Occultism", "IQ", "A", 0, "212", [O]],
          ["Religious Ritual", "IQ", "H", 0, "217", [O]],
          ["Ritual Magic", "IQ", "VH", 0, "218", [O]],
          ["Symbol Drawing", "IQ", "H", 0, "224", [O]],
          ["Thaumatology", "IQ", "VH", 0, "225", [O]],
          ["Acting", "IQ", "A", 0, "174", [S]],
          ["Administration", "IQ", "A", 0, "174", [S]],
          ["Body Language", "Per", "A", 0, "181", [S]],
          ["Carousing", "HT", "E", 0, "183", [S]],
          ["Connoisseur", "IQ", "A", 0, "185", [S]],
          ["Detect Lies", "Per", "H", 0, "187", [O]],
          ["Diplomacy", "IQ", "H", 0, "187", [O]],
          ["Erotic Art", "DX", "A", 0, "192", [O]],
          ["Fast-Talk", "IQ", "A", 0, "195", [O]],
          ["Fortune-Telling", "IQ", "A", 0, "196", [O]],
          ["Gambling", "IQ", "A", 0, "197", [O]],
          ["Gesture", "IQ", "E", 0, "198", [O]],
          ["Heraldry", "IQ", "A", 0, "199", [O]],
          ["Intimidation", "Will", "A", 0, "202", [O,A,c]],
          ["Leadership", "IQ", "A", 0, "204", [O]],
          ["Merchant", "IQ", "A", 0, "209", [O]],
          ["Panhandling", "IQ", "E", 0, "212", [O]],
          ["Politics", "IQ", "A", 0, "215", [O]],
          ["Propaganda/TL", "IQ", "A", 0, "216", [O]],
          ["Public Speaking", "IQ", "A", 0, "216", [O]],
          ["Savoir-Faire", "IQ", "E", 0, "218", [O]],
          ["Sex Appeal", "HT", "A", 0, "219", [O]],
          ["Streetwise", "IQ", "A", 0, "223", [O]],
          ["Teaching", "IQ", "A", 0, "224", [O]],
          ]


SKILL_CATEGORIES = [A,B,C,D,M,T,S,O,G]







