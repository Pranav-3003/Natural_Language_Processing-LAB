"""
Dataset Generator for PolluAlert
Generates a student-curated academic dataset of ~500 pollution-related texts.
This script creates the dataset programmatically for reproducibility.
"""

import csv
import os
import random

# Seed for reproducibility
random.seed(42)

# ============================================================
# DATASET RECORDS
# Each record: (text, pollution_type, severity, emergency_status, location, source_type)
# ============================================================

records = [
    # ===================== AIR POLLUTION =====================
    # LOW severity
    ("There is some dust in the air near the construction site.", "Air Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Mild smoke smell noticed in the neighbourhood this morning.", "Air Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Some vehicles on the highway are producing visible exhaust fumes.", "Air Pollution", "LOW", "POLLUTION REPORT", "Not specified", "observation"),
    ("The air quality seems slightly poor today in the city area.", "Air Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("A few trucks were releasing black smoke while passing through the market.", "Air Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Dust particles are visible in the air near the unpaved road.", "Air Pollution", "LOW", "POLLUTION REPORT", "Not specified", "observation"),
    ("There is a faint burning smell in the air this evening.", "Air Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The local bakery chimney is emitting more smoke than usual.", "Air Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Light haze observed in the morning near the agricultural fields.", "Air Pollution", "LOW", "POLLUTION REPORT", "Not specified", "observation"),
    ("Some residents have noticed increased dust due to nearby construction.", "Air Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The air smells slightly smoky in the residential colony.", "Air Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Minor vehicle exhaust pollution observed near the bus stop.", "Air Pollution", "LOW", "POLLUTION REPORT", "Not specified", "observation"),

    # MEDIUM severity
    ("Thick smoke has been coming from the brick kiln for several hours.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Dense black smoke is rising from the industrial area near Pune highway.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Pune", "citizen_report"),
    ("Residents of Andheri East are complaining about continuous smoke from a nearby factory.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Andheri East", "news_report"),
    ("Smoke from crop burning is affecting visibility on the main road.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The area near the cement plant has very poor air quality with visible particles.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Multiple complaints received about smoke from the power plant in Nashik.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Nashik", "official_report"),
    ("Persistent smog covering the downtown area for the past two days.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "news_report"),
    ("Black smoke rising from an open waste burning site near the school.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Emissions from the steel factory are causing visibility issues on the road.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Farmers burning crop residue causing heavy smoke in Haryana region.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Haryana", "news_report"),
    ("The neighbourhood has been covered in smoke from the nearby tyre recycling unit.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Air pollution levels seem very high today in the market area with hazy conditions.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "observation"),
    ("There is continuous smoke emission from the sugar factory chimney.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # HIGH severity
    ("Extremely thick black smoke from the chemical factory is covering the entire locality and people are coughing.", "Air Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("Massive fire at the warehouse is producing toxic smoke spreading over several kilometres near Mumbai.", "Air Pollution", "HIGH", "POTENTIAL EMERGENCY", "Mumbai", "news_report"),
    ("Dense poisonous smoke from burning plastic waste is causing severe breathing difficulties among residents.", "Air Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("A large industrial fire near Ambernath is producing hazardous smoke affecting thousands of people.", "Air Pollution", "HIGH", "POTENTIAL EMERGENCY", "Ambernath", "news_report"),
    ("People in Bhiwandi are experiencing severe respiratory problems due to toxic fumes from a factory fire.", "Air Pollution", "HIGH", "POTENTIAL EMERGENCY", "Bhiwandi", "news_report"),
    ("Thick smoke from burning tyres is making it impossible to breathe in the area.", "Air Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("Severe air pollution emergency as factory emissions reach dangerous levels.", "Air Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "official_report"),
    ("Toxic gas release from the industrial zone is affecting nearby residential areas.", "Air Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),

    # ===================== WATER POLLUTION =====================
    # LOW severity
    ("The pond water near the park looks slightly greenish.", "Water Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("There seems to be some algae growing in the community lake.", "Water Pollution", "LOW", "POLLUTION REPORT", "Not specified", "observation"),
    ("The tap water has a slightly unusual taste today.", "Water Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Some foam was noticed on the surface of the river near the bridge.", "Water Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The well water appears slightly cloudy after recent rains.", "Water Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Minor oil sheen observed on the canal water surface.", "Water Pollution", "LOW", "POLLUTION REPORT", "Not specified", "observation"),
    ("The stream near the village has some floating debris.", "Water Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Residents noticed mild discolouration of water in the storage tank.", "Water Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("A small amount of waste water seems to be leaking into the drain.", "Water Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The lake water has become slightly murky compared to last month.", "Water Pollution", "LOW", "POLLUTION REPORT", "Not specified", "observation"),

    # MEDIUM severity
    ("The river water near Sangam Nagar has turned dark brown and smells very bad.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Sangam Nagar", "citizen_report"),
    ("A factory is discharging waste water directly into the river near Kolhapur.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Kolhapur", "citizen_report"),
    ("Dead fish found floating in the lake near the industrial estate.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "news_report"),
    ("The drainage system near the hospital is overflowing into the nearby water body.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Sewage water is mixing with the drinking water supply in Ward 15.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Ward 15", "citizen_report"),
    ("The river near Aurangabad has thick foam forming on the surface.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Aurangabad", "news_report"),
    ("Industrial effluent is being released into the stream without treatment.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The canal water near MIDC area has changed colour to reddish brown.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "MIDC", "citizen_report"),
    ("Residents of Solapur complain that the river water has a strong chemical smell.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Solapur", "citizen_report"),
    ("The municipal corporation drain is discharging untreated waste into the lake.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "official_report"),
    ("Water in the bore well near the factory has turned yellowish.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Multiple dead fish and foul smell reported from the village pond.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # HIGH severity
    ("Massive chemical discharge from the paint factory has contaminated the entire river and hundreds of fish are dead.", "Water Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),
    ("Toxic industrial waste has contaminated the drinking water supply affecting over 500 families in Nagpur.", "Water Pollution", "HIGH", "POTENTIAL EMERGENCY", "Nagpur", "news_report"),
    ("Several children have fallen ill after drinking contaminated water from the village well near the chemical plant.", "Water Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),
    ("A major pipeline leak has caused crude oil to spill into the river near Ratnagiri.", "Water Pollution", "HIGH", "POTENTIAL EMERGENCY", "Ratnagiri", "news_report"),
    ("The entire village water supply has been contaminated with industrial chemicals causing widespread illness.", "Water Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("People have been hospitalized after consuming water from the polluted lake near the textile factory.", "Water Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),
    ("Chemical dye waste from the factory is flowing directly into the drinking water reservoir.", "Water Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("Hazardous waste leaked into the groundwater supply contaminating water for an entire block.", "Water Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "official_report"),

    # ===================== SOIL/LAND POLLUTION =====================
    # LOW severity
    ("There is some litter scattered around the empty plot near the school.", "Soil/Land Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("A few plastic bags and bottles are lying in the open field.", "Soil/Land Pollution", "LOW", "POLLUTION REPORT", "Not specified", "observation"),
    ("The garden soil near the factory gate seems slightly discoloured.", "Soil/Land Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Some construction debris has been left in the vacant land.", "Soil/Land Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("There are scattered plastic wrappers and waste in the open ground.", "Soil/Land Pollution", "LOW", "POLLUTION REPORT", "Not specified", "observation"),
    ("Minor soil erosion observed near the construction site.", "Soil/Land Pollution", "LOW", "POLLUTION REPORT", "Not specified", "observation"),
    ("Old batteries and electronic parts found dumped in the empty lot.", "Soil/Land Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The soil near the petrol pump appears slightly oily.", "Soil/Land Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # MEDIUM severity
    ("Large quantities of industrial waste have been dumped on agricultural land near Ahmednagar.", "Soil/Land Pollution", "MEDIUM", "POLLUTION REPORT", "Ahmednagar", "citizen_report"),
    ("The soil in the area around the abandoned factory has turned black and has a chemical smell.", "Soil/Land Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Illegal dumping of factory waste on farmland has been reported by farmers in Satara.", "Soil/Land Pollution", "MEDIUM", "POLLUTION REPORT", "Satara", "citizen_report"),
    ("Oil and grease waste from the automobile workshop is contaminating the surrounding soil.", "Soil/Land Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Fly ash from the power plant is being dumped on open land affecting nearby crops.", "Soil/Land Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Mining activities have left the land barren and contaminated in the area.", "Soil/Land Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "news_report"),
    ("Chemical residue from the pesticide factory is seeping into the agricultural fields.", "Soil/Land Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The landfill site near Pimpri has expanded beyond its boundary contaminating surrounding land.", "Soil/Land Pollution", "MEDIUM", "POLLUTION REPORT", "Pimpri", "official_report"),

    # HIGH severity
    ("Toxic chemical waste has been illegally buried in the farmland and crops are dying in the entire region.", "Soil/Land Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),
    ("Hazardous industrial sludge dumped near the school playground is causing skin rashes among children.", "Soil/Land Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),
    ("Major oil spill on agricultural land has destroyed crops over 50 acres near Sangli.", "Soil/Land Pollution", "HIGH", "POTENTIAL EMERGENCY", "Sangli", "news_report"),
    ("Radioactive waste material found dumped illegally near the residential area.", "Soil/Land Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "official_report"),
    ("Large scale illegal dumping of toxic chemicals has contaminated the soil and groundwater.", "Soil/Land Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),

    # ===================== NOISE POLLUTION =====================
    # LOW severity
    ("The traffic noise on the main road is quite loud during rush hours.", "Noise Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Construction work next door has been making noise during the day.", "Noise Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The neighbourhood dogs are barking loudly at night.", "Noise Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("There is moderate noise from the nearby workshop during working hours.", "Noise Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Music from the restaurant is slightly loud in the evening.", "Noise Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Some noise from the generator can be heard in the neighbourhood.", "Noise Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The highway traffic creates a constant hum in the background.", "Noise Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Occasional loud honking from vehicles near the market area.", "Noise Pollution", "LOW", "POLLUTION REPORT", "Not specified", "observation"),

    # MEDIUM severity
    ("Extremely loud music from the marriage hall is continuing past midnight disturbing the entire area.", "Noise Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The factory machines are producing very loud noise round the clock in the residential neighbourhood.", "Noise Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Continuous blasting from the quarry near Latur is shaking houses and causing distress.", "Noise Pollution", "MEDIUM", "POLLUTION REPORT", "Latur", "citizen_report"),
    ("Night time construction work on the highway is producing unbearable noise levels in nearby villages.", "Noise Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The stone crushing unit is generating excessive noise affecting residents of the colony.", "Noise Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Multiple DJ sound systems operating simultaneously during the festival causing extreme noise.", "Noise Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Industrial machinery noise from the MIDC area near Jalgaon is affecting nearby schools.", "Noise Pollution", "MEDIUM", "POLLUTION REPORT", "Jalgaon", "citizen_report"),
    ("Heavy machinery operating throughout the night near the hospital area.", "Noise Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # HIGH severity
    ("Continuous extremely loud industrial noise causing hearing problems among factory workers and nearby residents.", "Noise Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),
    ("Residents near the airport runway are reporting hearing damage due to constant aircraft noise.", "Noise Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),
    ("Blasting operations at the mine have caused structural damage to nearby houses and noise-induced injuries.", "Noise Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),
    ("Prolonged exposure to extreme noise from the steel plant has led to multiple hearing loss cases.", "Noise Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),

    # ===================== INDUSTRIAL POLLUTION =====================
    # LOW severity
    ("A small factory is producing some smoke during its operations.", "Industrial Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("There is a mild chemical smell coming from the workshop area.", "Industrial Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The small manufacturing unit seems to be releasing some waste water into the drain.", "Industrial Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Minor vibrations felt from the industrial machinery in the adjacent building.", "Industrial Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Light grey smoke observed from the small factory chimney.", "Industrial Pollution", "LOW", "POLLUTION REPORT", "Not specified", "observation"),
    ("The paint shop is emitting some fumes during working hours.", "Industrial Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("A mild odour is coming from the food processing unit down the street.", "Industrial Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Some dust being generated by the stone cutting unit in the area.", "Industrial Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # MEDIUM severity
    ("The chemical factory in MIDC Ahmednagar is releasing foul-smelling emissions regularly.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Ahmednagar", "citizen_report"),
    ("Residents near the paper mill in Raigad are complaining about strong sulphur smell.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Raigad", "citizen_report"),
    ("The sugar factory is discharging untreated effluent into the nearby canal.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Dense smoke from the foundry unit is affecting the visibility and air quality of the residential area.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The textile dyeing unit is releasing coloured waste water into the stream near Ichalkaranji.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Ichalkaranji", "citizen_report"),
    ("Multiple factories in the industrial belt are violating emission norms.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "official_report"),
    ("The pharmaceutical company is generating excessive waste which is not being properly disposed.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Heavy dust and noise from the cement factory is affecting the nearby village.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The metal plating factory is releasing acidic waste water without treatment.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Smoke and particulate matter from the brick kiln is causing air quality issues.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # HIGH severity
    ("Major industrial accident at the chemical plant near Chembur has released toxic gases affecting thousands.", "Industrial Pollution", "HIGH", "POTENTIAL EMERGENCY", "Chembur", "news_report"),
    ("Factory explosion in Tarapur MIDC has caused massive fire and toxic chemical release into the environment.", "Industrial Pollution", "HIGH", "POTENTIAL EMERGENCY", "Tarapur", "news_report"),
    ("Residents near the MIDC Dombivli reported thick toxic smoke from a chemical factory causing mass evacuation.", "Industrial Pollution", "HIGH", "POTENTIAL EMERGENCY", "Dombivli", "news_report"),
    ("A major chemical spill at the industrial plant has contaminated the river and several people have been hospitalized.", "Industrial Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),
    ("Toxic gas leak from the pesticide factory has caused breathing emergencies in the surrounding area.", "Industrial Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),
    ("Industrial waste fire at the dump site is producing highly toxic smoke spreading over the residential area.", "Industrial Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("Explosion at the refinery near Jamnagar has caused oil leak and fire contaminating the coastal area.", "Industrial Pollution", "HIGH", "POTENTIAL EMERGENCY", "Jamnagar", "news_report"),

    # ===================== WASTE/GARBAGE POLLUTION =====================
    # LOW severity
    ("Some garbage has been thrown near the roadside.", "Waste/Garbage Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("A few plastic bags are lying around the park bench.", "Waste/Garbage Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("There is some litter near the bus stop area.", "Waste/Garbage Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Food waste has been dumped in the empty plot next to our building.", "Waste/Garbage Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("A small pile of garbage is accumulating at the street corner.", "Waste/Garbage Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Some household waste bags are left outside the designated collection area.", "Waste/Garbage Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Litter is scattered around the picnic spot near the lake.", "Waste/Garbage Pollution", "LOW", "POLLUTION REPORT", "Not specified", "observation"),
    ("A dustbin near the market is overflowing with waste.", "Waste/Garbage Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("There is some garbage dumped on the vacant plot beside the temple.", "Waste/Garbage Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Plastic waste found near the walking track in the garden.", "Waste/Garbage Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # MEDIUM severity
    ("A large amount of garbage has been dumped near the school in Hadapsar.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Hadapsar", "citizen_report"),
    ("The municipal garbage collection has not happened for a week and waste is piling up in the colony.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Illegal dumping of construction debris and waste near the river bank.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Large garbage dump near the residential area is attracting stray animals and causing hygiene issues.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The waste collection point near Katraj has become a permanent dumping ground with rotting waste.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Katraj", "citizen_report"),
    ("Open dumping of garbage near the water tank is creating foul smell and health hazards.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Household and commercial waste is being thrown into the nullah near the market area.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Large scale littering and waste accumulation at the weekly market site.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The garbage processing plant in Kothrud has stopped working and waste is accumulating.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Kothrud", "citizen_report"),
    ("Tonnes of unprocessed waste lying in open area near the housing society.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # HIGH severity
    ("Massive illegal garbage dump near the hospital is burning and creating toxic smoke affecting patients.", "Waste/Garbage Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),
    ("Medical waste including syringes and bandages found dumped openly near the school playground.", "Waste/Garbage Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),
    ("Biomedical waste from the clinic is being thrown into the municipal garbage bin contaminating the area.", "Waste/Garbage Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("A mountain of garbage has collapsed at the landfill site trapping several waste pickers.", "Waste/Garbage Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),
    ("Burning garbage dump near residential area in Bhosari releasing toxic fumes and causing mass breathing problems.", "Waste/Garbage Pollution", "HIGH", "POTENTIAL EMERGENCY", "Bhosari", "news_report"),
    ("Hazardous chemical containers found in regular municipal waste dump near populated area.", "Waste/Garbage Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "official_report"),

    # ===================== CHEMICAL POLLUTION =====================
    # LOW severity
    ("There is a mild chemical smell near the cleaning supply store.", "Chemical Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("A faint paint smell is coming from the auto body shop.", "Chemical Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Slight chemical odour noticed near the printing press.", "Chemical Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("There is a cleaning chemical smell in the corridor after floor washing.", "Chemical Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Mild solvent smell coming from the furniture workshop.", "Chemical Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("A slight chemical smell is noticeable near the agricultural supply store.", "Chemical Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Faint pesticide smell drifting from the nearby farm during spraying season.", "Chemical Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Minor fuel smell near the petrol station noticed by pedestrians.", "Chemical Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # MEDIUM severity
    ("Strong chemical smell is spreading in the area around the textile factory in Bhiwandi.", "Chemical Pollution", "MEDIUM", "POLLUTION REPORT", "Bhiwandi", "citizen_report"),
    ("Chemical waste drums are stored improperly in an open area near residential buildings.", "Chemical Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("A persistent chemical smell from the pesticide manufacturing unit is making residents uncomfortable.", "Chemical Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Chemical runoff from the factory is visible in the drainage near Pimpri-Chinchwad.", "Chemical Pollution", "MEDIUM", "POLLUTION REPORT", "Pimpri-Chinchwad", "citizen_report"),
    ("The paint factory is emitting strong chemical fumes especially during night shifts.", "Chemical Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Residents are complaining about a continuous chemical smell from the pharmaceutical unit.", "Chemical Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("A chemical spill was observed on the road near the industrial area.", "Chemical Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The acid processing unit is releasing fumes that are irritating the eyes of nearby residents.", "Chemical Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Chemical containers are being washed in the open near the river bank.", "Chemical Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Industrial chemicals stored in the open are leaking during rains contaminating the area.", "Chemical Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # HIGH severity
    ("A chemical leak in the factory has caused a toxic cloud and people are having severe difficulty breathing.", "Chemical Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("Major acid spill from the tanker on the highway near Panvel is causing burns to people in contact.", "Chemical Pollution", "HIGH", "POTENTIAL EMERGENCY", "Panvel", "news_report"),
    ("Chlorine gas leak from the water treatment plant has caused mass evacuation near Thane.", "Chemical Pollution", "HIGH", "POTENTIAL EMERGENCY", "Thane", "news_report"),
    ("A chemical explosion at the factory has released hazardous substances into the air and water.", "Chemical Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),
    ("Ammonia gas leak at the cold storage facility is causing respiratory emergencies in the surrounding area.", "Chemical Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),
    ("Toxic chemical fumes from the warehouse fire are spreading rapidly across multiple neighbourhoods.", "Chemical Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("Large scale chemical contamination detected in residential water supply after factory accident.", "Chemical Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "official_report"),
    ("Chemical leak has caused a strong toxic smell and several people are having breathing problems.", "Chemical Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("Pesticide gas leak at the godown has caused unconsciousness among workers and nearby people.", "Chemical Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),

    # ===================== OTHER/UNKNOWN =====================
    # LOW severity
    ("There is some unusual smell in the area but cannot identify the source.", "Other/Unknown", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Something seems off about the environment in this area but not sure what.", "Other/Unknown", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("An unidentified substance has been noticed on the ground near the road.", "Other/Unknown", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("There is a strange odour in the neighbourhood that comes and goes.", "Other/Unknown", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Some kind of residue is visible on the walls of the buildings near the factory.", "Other/Unknown", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("An unusual coloured substance is seeping from the ground.", "Other/Unknown", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # MEDIUM severity
    ("Unidentified waste material is being dumped at night in the area behind the market.", "Other/Unknown", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("An unknown source of pollution is causing discomfort among residents of the housing complex.", "Other/Unknown", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Unidentified thick liquid flowing from an unknown source into the stormwater drain.", "Other/Unknown", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Multiple residents reporting unusual health symptoms possibly related to environmental contamination.", "Other/Unknown", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Unknown pollutant making the air quality visibly poor in the neighbourhood.", "Other/Unknown", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # HIGH severity
    ("Unknown substance leak causing mass nausea and dizziness among residents urgent help needed.", "Other/Unknown", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("Unidentified toxic fumes causing people to collapse in the area immediate evacuation needed.", "Other/Unknown", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("Unknown chemical exposure causing severe skin burns and breathing difficulties in multiple people.", "Other/Unknown", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),

    # ===================== NORMAL (NOT POLLUTION) =====================
    ("Today is a beautiful sunny day and the weather is pleasant.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The flowers in the garden are blooming nicely this season.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("I went to the park for my morning walk and it was very refreshing.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The new road construction in the city is progressing well.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("Our school organized a tree planting drive last weekend.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The local market was very crowded during the festival season.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("I enjoyed a nice meal at the new restaurant near the station.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The cricket match yesterday was very exciting.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("Students are preparing for their final examinations.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The new library in the college campus has been inaugurated.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("Traffic is moving smoothly on the expressway today.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The monsoon season has started and we received good rainfall.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("A new shopping complex has opened near the railway station.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The electricity supply has improved significantly in our area.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("Our society organized a sports competition for children last Sunday.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The hospital has started a free health check-up camp for senior citizens.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("I attended a workshop on digital marketing at the community centre.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The train service between Pune and Mumbai is very convenient.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The annual cultural festival at the college was a grand success.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("My family went on a trip to Mahabaleshwar and the weather was lovely.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The city has planted over 10000 trees this year as part of the green initiative.", "Not Pollution", "NONE", "NORMAL", "Not specified", "news_report"),
    ("The metro construction is expected to be completed by next year.", "Not Pollution", "NONE", "NORMAL", "Not specified", "news_report"),
    ("Students celebrated Republic Day with great enthusiasm at the college.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The new water supply pipeline has been laid in our colony.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The farmer market on Sunday had fresh vegetables and fruits.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("Our building society conducted its annual general meeting successfully.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("A new bus route has been started connecting the suburb to the city centre.", "Not Pollution", "NONE", "NORMAL", "Not specified", "news_report"),
    ("The vaccination drive at the health centre is going smoothly.", "Not Pollution", "NONE", "NORMAL", "Not specified", "news_report"),
    ("I helped my neighbour fix a leaking tap this morning.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The sunset view from the hill station was absolutely beautiful.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("Our college placed 85 percent of students in campus placements.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The local temple committee organized a grand festival last week.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The government has announced a new skill development programme for youth.", "Not Pollution", "NONE", "NORMAL", "Not specified", "news_report"),
    ("The mobile network coverage has improved in our rural area.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("I completed an online course in Python programming recently.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The blood donation camp at the hospital was well attended.", "Not Pollution", "NONE", "NORMAL", "Not specified", "news_report"),
    ("Our neighbours adopted a stray dog and named it Bruno.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The new flyover has reduced traffic congestion significantly.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("Children enjoyed the science exhibition organized by the school.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The yoga session in the park every morning is very beneficial.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("We had a wonderful family gathering during Diwali.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The municipal corporation has improved the street lighting in our area.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("I recently learned to cook a new recipe from an online video.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The river cleanup volunteer drive was very successful.", "Not Pollution", "NONE", "NORMAL", "Not specified", "news_report"),
    ("The weather forecast predicts a pleasant week ahead.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("A new art exhibition has opened at the city museum.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The local football team won the district level championship.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("Solar panels have been installed on the rooftop of our building.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("I had a productive day at work and completed all my tasks.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("The garden committee planted several fruit trees along the road.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),

    # ===================== ADDITIONAL MIXED / EDGE CASES =====================
    # Ambiguous cases
    ("There is a strange smell near the river but I am not sure what it is.", "Other/Unknown", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The water looks different today but it might just be the rain.", "Other/Unknown", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Something is burning somewhere in the area.", "Air Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The air does not feel right today.", "Other/Unknown", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # Multi-indicator cases
    ("Thick black smoke from a factory near the highway is visible and residents are feeling suffocated.", "Industrial Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("A strong chemical smell is spreading around the residential area and people are feeling dizzy.", "Chemical Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("The river water has become dark and smells very bad near Wai and fish are dying.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Wai", "citizen_report"),
    ("A large amount of garbage has been dumped near the school and it is attracting rats and insects.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("People living near the factory are complaining about smoke and developing skin problems.", "Industrial Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),

    # Additional Air Pollution
    ("Vehicular pollution on MG Road during peak hours is becoming unbearable.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "MG Road", "citizen_report"),
    ("Smoke from the nearby tandoor restaurant is filling up our apartment.", "Air Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The air quality index in Delhi NCR has crossed the severe category mark.", "Air Pollution", "HIGH", "POTENTIAL EMERGENCY", "Delhi NCR", "news_report"),
    ("Stubble burning in Punjab is causing severe air pollution in the region.", "Air Pollution", "HIGH", "POTENTIAL EMERGENCY", "Punjab", "news_report"),
    ("Crackers during Diwali have caused the air quality to deteriorate significantly.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # Additional Water Pollution
    ("The borewell water has a metallic taste and brownish colour near the battery factory.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Sewage overflow during monsoon is contaminating the water supply in the slum area.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The drinking water supplied by tanker has a strong chlorine smell today.", "Water Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Oil leak from the ship near the harbour is spreading on the sea surface.", "Water Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),

    # Additional Industrial Pollution
    ("The leather tannery in Kanpur is releasing untreated waste into the Ganga river.", "Industrial Pollution", "HIGH", "POTENTIAL EMERGENCY", "Kanpur", "news_report"),
    ("Cement dust from the factory is settling on crops and houses in the surrounding village.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The dyeing factory waste is turning the stream different colours every day.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # Additional Waste Pollution
    ("E-waste is being dismantled in the open near the market area without any safety measures.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Animal carcasses have been found dumped near the lake creating a health hazard.", "Waste/Garbage Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("The garbage van has not collected waste from our society for the past ten days.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Used plastic and packaging material from the online delivery hub is being burnt openly.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # Additional Chemical Pollution
    ("Pesticide spraying on crops near the school is causing headaches among students.", "Chemical Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Chemical tanker overturned on the highway leaking unknown substance.", "Chemical Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "news_report"),
    ("Strong bleach like chemical smell detected near the swimming pool area.", "Chemical Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # Additional Noise Pollution
    ("Loud speakers at the political rally are causing disturbance to residents.", "Noise Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The disco near our apartment plays loud music until 3 AM every night.", "Noise Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Firecrackers being burst continuously for hours during the wedding celebration.", "Noise Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # Additional Soil/Land Pollution
    ("The abandoned factory site has toxic waste buried underground which is now leaking.", "Soil/Land Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("Agricultural land near the tannery has become unfit for farming due to chemical contamination.", "Soil/Land Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Overuse of chemical fertilizers has degraded the soil quality in the farming area.", "Soil/Land Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # More edge cases - should be NORMAL or very low
    ("The government should invest more in renewable energy sources.", "Not Pollution", "NONE", "NORMAL", "Not specified", "social_media"),
    ("What are the main causes of air pollution in India?", "Not Pollution", "NONE", "NORMAL", "Not specified", "social_media"),
    ("I think we should all use electric vehicles to reduce pollution.", "Not Pollution", "NONE", "NORMAL", "Not specified", "social_media"),
    ("The environmental science lecture at college was very informative.", "Not Pollution", "NONE", "NORMAL", "Not specified", "citizen_report"),
    ("Pollution control board officials visited the factory for routine inspection.", "Not Pollution", "NONE", "NORMAL", "Not specified", "news_report"),

    # Additional multi-category pollution reports
    ("The factory is releasing both smoke into the air and waste into the river near Badlapur.", "Industrial Pollution", "HIGH", "POTENTIAL EMERGENCY", "Badlapur", "citizen_report"),
    ("Burning garbage on the roadside is creating smoke and ash is settling on nearby houses.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The chemical plant discharge has polluted both the soil and the groundwater.", "Chemical Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("Construction dust and heavy truck noise from the site is disturbing the entire neighbourhood.", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # More realistic citizen complaints
    ("I want to report that the nullah behind our building stinks badly especially in summer.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Please help, the factory next to our colony keeps releasing foul gas at night when nobody is watching.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Sir, there is a big garbage pile burning near our children's school and smoke is entering the classrooms.", "Waste/Garbage Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("We have been complaining for months about the textile unit dumping chemicals but no action has been taken.", "Chemical Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("The well water in our village has become poisonous after the factory started operations.", "Water Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("My child has developed asthma because of the constant smoke from the brick kilns nearby.", "Air Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("The noise from the stone quarry blasting is cracking the walls of our houses.", "Noise Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "citizen_report"),
    ("There is a foul smell coming from the drain but it is not too strong.", "Water Pollution", "LOW", "POLLUTION REPORT", "Not specified", "citizen_report"),
    ("Plastic waste is clogging the drainage system causing waterlogging during rains.", "Waste/Garbage Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "citizen_report"),

    # Social media style reports
    ("Why is there so much smoke near the MIDC area today? Anyone else noticing?", "Air Pollution", "MEDIUM", "POLLUTION REPORT", "MIDC", "social_media"),
    ("The river near our village looks like a drain now. So sad to see this.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "social_media"),
    ("Cannot sleep because of the construction noise going on at 1 AM. This is unacceptable.", "Noise Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "social_media"),
    ("Just saw a tanker dumping something into the lake. This should be reported.", "Water Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "social_media"),
    ("The whole area smells like chemicals today. Really worried about health effects.", "Chemical Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "social_media"),

    # Official/news style reports
    ("Pollution control board has issued notice to three factories for violating emission norms in Chakan.", "Industrial Pollution", "MEDIUM", "POLLUTION REPORT", "Chakan", "official_report"),
    ("Air quality monitoring shows PM2.5 levels exceeding safe limits in the industrial area.", "Air Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "official_report"),
    ("Water testing reveals high levels of heavy metals in groundwater near the industrial belt.", "Water Pollution", "HIGH", "POTENTIAL EMERGENCY", "Not specified", "official_report"),
    ("Environmental audit of the mining site reveals significant soil contamination.", "Soil/Land Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "official_report"),
    ("Noise level measurements near the airport show readings above permissible limits.", "Noise Pollution", "MEDIUM", "POLLUTION REPORT", "Not specified", "official_report"),
]


def generate_dataset():
    """Generate the pollution dataset CSV file."""
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "..", "data", "pollution_dataset.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Also ensure raw/ and processed/ directories exist
    os.makedirs(os.path.join(output_dir, "..", "data", "raw"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "..", "data", "processed"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "..", "models"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "..", "docs", "figures"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "..", "notebooks"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "..", "tests"), exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "text", "pollution_type", "severity", "emergency_status", "location", "source_type"])
        for i, (text, ptype, severity, emergency, location, source) in enumerate(records, 1):
            writer.writerow([i, text, ptype, severity, emergency, location, source])

    print(f"Dataset generated: {output_path}")
    print(f"Total records: {len(records)}")

    # Print class distribution
    from collections import Counter
    type_dist = Counter(r[1] for r in records)
    severity_dist = Counter(r[2] for r in records)
    emergency_dist = Counter(r[3] for r in records)

    print("\n--- Pollution Type Distribution ---")
    for k, v in sorted(type_dist.items()):
        print(f"  {k}: {v}")

    print("\n--- Severity Distribution ---")
    for k, v in sorted(severity_dist.items()):
        print(f"  {k}: {v}")

    print("\n--- Emergency Status Distribution ---")
    for k, v in sorted(emergency_dist.items()):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    generate_dataset()
