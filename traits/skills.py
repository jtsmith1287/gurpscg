

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

SKILLS = (["Name", "Attribute", "Difficulty", "TL", "Page", "Category"],
          ["Acting", "IQ", "A", 0, "174", [S]],
          ["Administration", "IQ", "A", 1, "174", [S]],
          ["Alchemy/TL", "IQ", "VH", 1, "174", [D,G,M,O]],
          ["Area Knowledge", "IQ", "E", 0, "176", [E]],
          ["Axe/Mace", "DX", "A",  1, "208", [A]],
          ["Body Language", "Per", "A", 0, "181", [S]],
          ["Boxing", "DX", "A", 1, "182", [C]],
          ["Brawling", "DX", "E",  0, "182", [C]],
          ["Broadsword", "DX", "A",  2, "208", [A]],
          ["Carousing", "HT", "E", 0, "183", [S]],
          ["Carpentry", "IQ", "E",  1, "208", [D]],
          ["Cloak", "DX", "A",  0, "184", [A, C]],
          ["Computer Operation/TL", "IQ", "E", 8, "184", [E, T]],
          ["Connoisseur", "IQ", "A", 1, "185", [S]],
          ["Cooking", "IQ", "A", 0, "185", [E, D]],
          ["Current Affairs/TL", "IQ", "E", 0, "186", [S,E]],
          ["Detect Lies", "Per", "H", 0, "187", [O]],
          ["Diagnosis/TL", "IQ", "H", 0, "187", [M]],
          ["Diplomacy", "IQ", "H", 0, "187", [O]],
          ["Electronics Operation/TL (Medical)", "IQ", "A", 8, "189", [T, M]],
          ["Erotic Art", "DX", "A", 0, "192", [O]],
          ["Esoteric Medicine", "Per", "H", 1, "192", [M]],
          ["Exorcism", "Will", "H", 1, "193", [O, M]],
          ["Expert Skill (Epidemiology)", "IQ", "H", 1, "193", [M]],
          ["Expert Skill (Psionics)", "IQ", "H", 0, "193", [G]],
          ["Fast-Draw", "DX", "E",  0, "194", [A, B]],
          ["Fast-Talk", "IQ", "A", 0, "195", [O]],
          ["First Aid/TL", "IQ", "E", 0, "195", [E]],
          ["Flail", "DX", "H",  1, "208", [A]],
          ["Force Sword", "DX", "A",  10, "208", [A]],
          ["Force Whip", "DX", "A",  10, "209", [A]],
          ["Fortune-Telling", "IQ", "A", 1, "196", [O]],
          ["Gambling", "IQ", "A", 0, "197", [O]],
          ["Garrote", "DX", "E",  3, "208", [C]],
          ["Gesture", "IQ", "E", 0, "198", [O]],
          ["Heraldry", "IQ", "A", 3, "199", [O]],
          ["Herb Lore/TL", "IQ", "VH", 0, "199", [O]],
          ["Hidden Lore (Demon Lore)", "IQ", "A", 1, "199", [O]],
          ["Hidden Lore (Faerie Lore)", "IQ", "A", 1, "199", [O]],
          ["Hidden Lore (Spirit Lore)", "IQ", "A", 1, "199", [O]],
          ["Housekeeping", "IQ", "E", 1, "200", [E]],
          ["Hypnotism", "IQ", "H", 3, "201", [O, M]],
          ["Intimidation", "Will", "A", 0, "202", [O,A,C]],
          ["Jitte/Sai", "DX", "A",  3, "208", [A]],
          ["Judo", "DX", "H",  2, "203", [C]],
          ["Karate", "DX", "H",  2, "203", [C]],
          ["Knife", "DX", "E",  0, "208", [A]],
          ["Knot-Tying", "DX", "E", 0, "203", [E,D]],
          ["Kusari", "DX", "H",  2, "209", [A]],
          ["Lance", "DX", "A",  3, "204", [A]],
          ["Leadership", "IQ", "A", 0, "204", [O]],
          ["Main-Gauche", "DX", "A",  3, "208", [A]],
          ["Merchant", "IQ", "A", 1, "209", [O]],
          ["Monowire Whip", "DX", "H",  11, "209", [A]],
          ["Occultism", "IQ", "A", 1, "212", [O]],
          ["Panhandling", "IQ", "E", 1, "212", [O]],
          ["Parry Missile Weapons", "DX", "H",  0, "212", [A]],
          ["Pharmacy/TL", "IQ", "H", 3, "213", [M]],
          ["Physician/TL", "IQ", "H", 1, "213", [M]],
          ["Physiology/TL", "IQ", "H", 1, "213", [M]],
          ["Poisons/TL", "IQ", "H", 0, "214", [M,D,O]],
          ["Polearm", "DX", "A",  1, "208", [A]],
          ["Politics", "IQ", "A", 1, "215", [O]],
          ["Propaganda/TL", "IQ", "A", 1, "216", [O]],
          ["Psychology", "IQ", "H", 3, "216", [M,O]],
          ["Public Speaking", "IQ", "A", 0, "216", [O]],
          ["Rapier", "DX", "A",  4, "208", [A]],
          ["Religious Ritual", "IQ", "H", 1, "217", [O,G]],
          ["Ritual Magic", "IQ", "VH", 1, "218", [O,G]],
          ["Saber", "DX", "A",  4, "208", [A]],
          ["Savoir-Faire", "IQ", "E", 0, "218", [S, E, O]],
          ["Sewing/TL", "DX", "E", 0, "219", [D, E]],
          ["Sex Appeal", "HT", "A", 0, "219", [O]],
          ["Shield", "DX", "E",  1, "220", [A]],
          ["Shortsword", "DX", "A",  1, "209", [A]],
          ["Smallsword", "DX", "A",  1, "208", [A]],
          ["Spear", "DX", "A",  1, "208", [A]],
          ["Staff", "DX", "A",  0, "208", [A]],
          ["Streetwise", "IQ", "A", 2, "223", [O]],
          ["Sumo Wrestling", "DX", "A",  3, "223", [C]],
          ["Surgery/TL", "IQ", "VH", 2, "223", [M,O]],
          ["Symbol Drawing", "IQ", "H", 0, "224", [O,G]],
          ["Teaching", "IQ", "A", 0, "224", [O]],
          ["Thaumatology", "IQ", "VH", 1, "225", [O,G]],
          ["Tonfa", "DX", "A",  6, "209", [A]],
          ["Two-Handed Axe/Mace", "DX", "A",  1, "208", [A]],
          ["Two-Handed Flail", "DX", "H",  1, "208", [A]],
          ["Two-Handed Sword", "DX", "A",  2, "209", [A]],
          ["Typing", "DX", "E", 7, "228", [T, E]],
          ["Veterinary/TL", "IQ", "H", 1, "228", [M]],
          ["Weather Sense", "IQ", "A", 0, "209", [E]],
          ["Whip", "DX", "A",  0, "209", [A]],
          ["Wrestling", "DX", "A",  0, "228", [C]],
          )


SKILL_CATEGORIES = [A,B,C,D,M,T,S,O,G]







