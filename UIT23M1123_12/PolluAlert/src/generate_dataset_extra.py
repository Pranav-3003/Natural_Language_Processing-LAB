"""
Additional dataset records for PolluAlert.
Adds more records to bring the total to ~500.
Run this after generate_dataset.py to append additional records.
"""

import csv
import os

additional_records = [
    # ===================== MORE AIR POLLUTION =====================
    ("Heavy smog blankets the city making it hard to see buildings across the street.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The wood processing unit is emitting sawdust and smoke into the air continuously.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Exhaust fumes from diesel generators during power cuts are polluting the apartment complex.", "Air Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The incinerator at the hospital is producing smoke with a very bad smell.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Dust storms from the quarry are making life miserable for the villagers.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("A rubber factory in Manchar is producing black acrid smoke polluting the surrounding farms.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Manchar", "citizen_report"),
    ("Garbage burning at the municipal dump is creating a thick layer of smoke over the township.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The asphalt plant on Solapur Road emits strong tar-like fumes every evening.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Solapur Road", "citizen_report"),
    ("Toxic fumes from the battery recycling unit are causing headaches and nausea among neighbours.", "Air Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("Forest fire near Mahabaleshwar is generating massive smoke clouds visible from the city.", "Air Pollution", "HIGH", "POTENTIAL EMERGENCY", "Mahabaleshwar", "news_report"),
    ("Coal dust from the thermal power plant is covering houses and crops in Chandrapur district.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Chandrapur", "news_report"),
    ("Burning of electronic waste in the open lot is releasing harmful fumes into the air.", "Air Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),

    # ===================== MORE WATER POLLUTION =====================
    ("The Mula river near Aundh bridge smells terrible due to untreated sewage discharge.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Aundh", "citizen_report"),
    ("Washing of chemical tankers in the open area is polluting nearby water sources.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Farmers downstream report that irrigation water from the canal has a chemical taste.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Detergent foam is accumulating on the river surface near the ghats.", "Water Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The reservoir water has turned green due to algae bloom possibly caused by fertiliser runoff.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Cyanide waste from the gold processing unit has reached the village well.", "Water Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),
    ("Raw sewage from the housing colony is directly flowing into the nullah near Hinjewadi.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Hinjewadi", "citizen_report"),
    ("People who drank water from the hand pump near the factory have developed stomach problems.", "Water Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("The colour of tap water has changed to yellowish in Wagholi area.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Wagholi", "citizen_report"),
    ("Floating oil patches visible on the creek near the port area.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "observation"),
    ("The river bed is covered with dark sludge from industrial discharge.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Groundwater contamination suspected after residents develop kidney problems near factory belt.", "Water Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),

    # ===================== MORE SOIL/LAND POLLUTION =====================
    ("Used engine oil from the auto garage is being poured on the ground daily.", "Soil/Land Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The area around the closed chemical factory has barren land where nothing grows.", "Soil/Land Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "observation"),
    ("Plastic mulch sheets used in farming are left in the fields decomposing into the soil.", "Soil/Land Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Heavy metal contamination found in soil samples near the electroplating unit.", "Soil/Land Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "official_report"),
    ("Asbestos sheets from the demolished building are lying in the open ground.", "Soil/Land Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The former gas station site has oil contaminated soil that has not been cleaned up.", "Soil/Land Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Excessive use of pesticides has made the farm soil infertile in Baramati region.", "Soil/Land Pollution", "MEDIUM", "POLLUTION REPORT", "Baramati", "citizen_report"),
    ("Slag from the iron smelting unit is dumped on the farmland affecting crops.", "Soil/Land Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Lead contamination detected in soil near the old battery manufacturing site.", "Soil/Land Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "official_report"),
    ("Plastic waste is being mixed into the soil at the construction landfill site.", "Soil/Land Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # ===================== MORE NOISE POLLUTION =====================
    ("Pile driving at the construction site is producing ear splitting noise all day.", "Noise Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The auto repair workshop runs heavy machinery at night causing sleep disruption.", "Noise Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Road widening work with jackhammers is generating unbearable noise for weeks.", "Noise Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The temple loudspeaker starts at 4 AM disturbing everyone in the locality.", "Noise Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Industrial compressors running at the neighbouring factory cause constant vibrations.", "Noise Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The newly opened gym plays extremely loud music disturbing the residential building.", "Noise Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Train horn at the unmanned level crossing is deafeningly loud and constant.", "Noise Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Multiple cement mixer trucks running simultaneously creating horrible noise levels.", "Noise Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("People near the industrial grinding unit are reporting tinnitus and hearing loss.", "Noise Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("The power loom machines in the basement run 24 hours causing constant noise.", "Noise Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # ===================== MORE INDUSTRIAL POLLUTION =====================
    ("The plastic recycling factory is emitting acrid fumes during the melting process.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Runoff from the industrial estate is carrying pollutants into the agricultural canal.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The poultry processing plant is discharging waste into the open drain causing terrible stench.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The glass factory kiln is glowing all night and emitting heat and fumes.", "Industrial Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Emission from the sponge iron factory in Raigarh has blackened surrounding buildings.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Raigarh", "citizen_report"),
    ("Boiler explosion at the sugar factory released steam and pollutants injuring workers.", "Industrial Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),
    ("The fish processing unit smell is unbearable and spreading across the neighbourhood.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Chemical vapour escaping from faulty pipes at the refinery poses health risk.", "Industrial Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "official_report"),
    ("The soap manufacturing unit is releasing lye waste into the municipal drainage.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Hot metal slag being dumped in the open by the foundry is a fire and pollution hazard.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The fertilizer plant near Zuarinagar is emitting sulphur dioxide fumes affecting residents.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Zuarinagar", "citizen_report"),
    ("Unauthorized stone crusher operating near the national park causing dust and noise.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "official_report"),

    # ===================== MORE WASTE/GARBAGE POLLUTION =====================
    ("Chicken waste from the slaughterhouse is being thrown into the open gutter.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The composting facility is not working properly and rotting waste is piling up.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Discarded paint cans and thinner bottles found dumped near the children's playground.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The waste segregation is not being followed and everything is mixed in one dump.", "Waste/Garbage Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Old furniture and mattresses have been dumped on the roadside blocking the footpath.", "Waste/Garbage Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Sanitary waste is visible in the open garbage dump near the bus stop.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The community dustbin has not been emptied for days and garbage is overflowing onto the road.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Glass bottles and sharp objects in the dumped waste near the park are a danger to children.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Hospital waste bags seen in the regular municipal dump site near Chinchwad.", "Waste/Garbage Pollution", "HIGH", "POTENTIAL EMERGENCY", "Chinchwad", "citizen_report"),
    ("Flyblown meat waste from the market is attracting vultures and creating hygiene problems.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Construction demolition waste blocks the entire lane and nobody is clearing it.", "Waste/Garbage Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Styrofoam packaging waste is being blown by wind into the lake.", "Waste/Garbage Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # ===================== MORE CHEMICAL POLLUTION =====================
    ("The pesticide godown near the farm is leaking and contaminating the soil.", "Chemical Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Battery acid was spilled on the road near the recycling centre.", "Chemical Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Workers at the dye factory are developing skin diseases due to chemical exposure.", "Chemical Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("Formaldehyde smell from the furniture factory is giving headaches to nearby residents.", "Chemical Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Mercury from the thermometer factory was found in the drainage system.", "Chemical Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "official_report"),
    ("The agricultural chemical storage near Baramati burst due to heat releasing toxic fumes.", "Chemical Pollution", "HIGH", "POTENTIAL EMERGENCY", "Baramati", "news_report"),
    ("Paint thinner smell is very strong near the automobile painting booth.", "Chemical Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Acid fumes from the electroplating unit are corroding nearby metal structures.", "Chemical Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The fertilizer storage unit is emitting ammonia smell detectable from a kilometre away.", "Chemical Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Spilled laboratory chemicals near the university are creating foul odour.", "Chemical Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # ===================== MORE OTHER/UNKNOWN =====================
    ("There is an odd vibration felt in the ground near the construction site.", "Other/Unknown", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Something is wrong with the environment here but I cannot pinpoint the issue.", "Other/Unknown", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("An unpleasant sensation when stepping outside that was not there before.", "Other/Unknown", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Plants and trees in the neighbourhood are dying for no apparent reason.", "Other/Unknown", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Birds have stopped visiting the area which used to have many bird species.", "Other/Unknown", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Unusual number of residents falling sick at the same time in the building.", "Other/Unknown", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The street lamps are attracting an unusual number of insects at night.", "Other/Unknown", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # ===================== MORE NORMAL (NOT POLLUTION) =====================
    ("The new sports complex near the stadium is amazing for morning exercise.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("Our college organized an awareness programme on environmental conservation.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The food at the college canteen has improved after the new management took over.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("Reading about climate change in the newspaper makes me think about the future.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("My brother got a new job at an environmental consulting firm.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("We planted saplings in our building compound as part of environment day.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The swimming pool at the club has been cleaned and is ready for summer.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("Our apartment society has started rainwater harvesting this monsoon.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The air purifier in our office is working well and the indoor air feels fresh.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The documentary on ocean life was very interesting to watch.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("I am learning about machine learning and NLP in my computer science course.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The cleanliness drive organized by NGO in the village was very successful.", "Not Pollution", "NONE", "NORMAL", "Not specified", "news_report"),
    ("The wind energy project near Satara is generating electricity for the region.", "Not Pollution", "NONE", "NORMAL", "Not specified", "news_report"),
    ("Public transport usage has increased after the new bus routes were introduced.", "Not Pollution", "NONE", "NORMAL", "Not specified", "news_report"),
    ("I walked by the river today and the water looked clean and clear.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The recycling centre in our neighbourhood is doing a great job.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("Solar street lights have been installed in our village saving electricity.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The organic farm near Mulshi produces very fresh and healthy vegetables.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The electric bus service launched in the city is quiet and comfortable.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The environment minister inaugurated the new sewage treatment plant.", "Not Pollution", "NONE", "NORMAL", "Not specified", "news_report"),

    # ===================== MORE EDGE CASES =====================
    ("The factory is not polluting but the traffic near it creates a lot of dust.", "Air Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("I do not think the water is contaminated but it tastes a bit odd.", "Other/Unknown", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The smell is not very strong but it is definitely not normal.", "Other/Unknown", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("It is not an emergency but someone should look into the waste dumping issue.", "Waste/Garbage Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The noise is tolerable during the day but becomes very loud at night.", "Noise Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Not sure if this is pollution but the river colour has been changing daily.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("There is no visible pollution but residents have been feeling unwell lately.", "Other/Unknown", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # More diverse locations
    ("Chemical discharge spotted in Yamuna river near Mathura.", "Chemical Pollution", "MEDIUM", "POLLUTION REPORT", "Mathura", "news_report"),
    ("Air pollution complaints rising in Andheri West near the commercial zone.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Andheri West", "news_report"),
    ("Illegal sand mining on the river bed near Shirur is causing erosion.", "Soil/Land Pollution", "MEDIUM", "POLLUTION REPORT", "Shirur", "news_report"),
    ("Residents of Viman Nagar complain about aircraft noise at odd hours.", "Noise Pollution", "MEDIUM", "POLLUTION REPORT", "Viman Nagar", "citizen_report"),
    ("Garbage pile up in Kharadi IT park area due to contractor dispute.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Kharadi", "news_report"),
    ("Untreated sewage flowing into Mutha river near Sinhagad Road.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Sinhagad Road", "citizen_report"),
    ("Dust from marble cutting factories in Rajsamand affecting local population.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Rajsamand", "news_report"),
    ("Mercury contamination found in Kodaikanal lake from thermometer factory waste.", "Chemical Pollution", "HIGH", "POTENTIAL EMERGENCY", "Kodaikanal", "news_report"),
    ("Massive oil spill reported off the coast of Chennai affecting marine life.", "Water Pollution", "HIGH", "POTENTIAL EMERGENCY", "Chennai", "news_report"),
    ("Toxic gas leak at Visakhapatnam chemical plant causing mass evacuations.", "Chemical Pollution", "HIGH", "POTENTIAL EMERGENCY", "Visakhapatnam", "news_report"),
]


def append_to_dataset():
    """Append additional records to the existing dataset."""
    dataset_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "pollution_dataset.csv")

    # Read existing records to get the last ID
    existing_count = 0
    with open(dataset_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            existing_count += 1

    # Append new records
    with open(dataset_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for i, (text, ptype, severity, emergency, location, source) in enumerate(additional_records, existing_count + 1):
            writer.writerow([i, text, ptype, severity, emergency, location, source])

    total = existing_count + len(additional_records)
    print(f"Appended {len(additional_records)} records. Total now: {total}")

    # Print updated distribution
    from collections import Counter
    all_records = []
    with open(dataset_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_records.append(row)

    type_dist = Counter(r["pollution_type"] for r in all_records)
    severity_dist = Counter(r["severity"] for r in all_records)
    emergency_dist = Counter(r["emergency_status"] for r in all_records)

    print(f"\n--- Final Pollution Type Distribution ({len(all_records)} records) ---")
    for k, v in sorted(type_dist.items()):
        print(f"  {k}: {v}")

    print("\n--- Final Severity Distribution ---")
    for k, v in sorted(severity_dist.items()):
        print(f"  {k}: {v}")

    print("\n--- Final Emergency Status Distribution ---")
    for k, v in sorted(emergency_dist.items()):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    append_to_dataset()
