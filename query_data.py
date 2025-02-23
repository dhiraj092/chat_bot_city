import streamlit as st
import os
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Verify API key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("OPENAI_API_KEY environment variable is not set.")
    st.error("Error: API key is missing. Please check your .env file.")
    st.stop()


NOISE_REGULATION_TEXT = """
Noise Bylaw
Bylaw #: 2004-52

Description: Regulates noise in the City of Kingston.

Date passed: March 2, 2004

Disclaimer: Bylaws contained in this section have been prepared for research and reference purposes only. The original Noise Bylaw in pdf format is available from the Ofice of the City Clerk upon request.

Introduction

Whereas section 129 of the Municipal Act, 2001 authorizes the council of every local municipality to regulate and prohibit with respect to noise; and

Whereas section 434.1(1) of the Municipal Act, 2001, as amended from time to time, provides that a municipality may require a person, subject to such conditions as the municipality considers appropriate, to pay an administrative penalty if the municipality is satisfed that the person has failed to comply with a bylaw of the municipality passed under this Act;

Therefore the Council of The Corporation of the City of Kingston enacts as follows:

Part 1 - Defnitions

For the purposes of this Bylaw:

Administrative Penalty means an administrative penalty administered pursuant to "Bylaw 2020-69 of the Corporation of City of Kingston being “A Bylaw to Establish a Process for Administrative Penalties”

Agricultural property means a property that is zoned for agricultural use in the zoning bylaw that applies to the property;

Chief Fire Oficial means the assistant to the Fire Marshal who is the Fire Chief of the City of Kingston, or a member or members of Kingston Fire and Rescue appointed by the Fire Chief to be Chief Fire Oficials, subject to the limitations and conditions as are set out in the appointment.

City and City of Kingston mean The Corporation of the City of Kingston, as incorporated on January 1, 1998, and all of its administrative units;

Construction includes erection, alteration, repair, dismantling, demolition, structural maintenance, painting, moving, land clearing, earth moving, grading, excavation, blasting and detonation of explosive devices other than freworks, the laying of pipe and conduit whether above or below ground level, street and highway building, concreting, equipment installation and alteration and the structural installation of construction components and materials in any form or for any purpose, and includes any associated or related work;

Construction equipment means any equipment or device designed and intended for use in construction or material handling, including but not limited to air compressors, pile drivers,

pneumatic or hydraulic tools, bulldozers, tractors, excavators, trenchers, cranes, derricks, loaders, scrapers, pavers, generators, of-highway haulers, trucks, ditchers, compactors and rollers, pumps, concrete mixers, graders or other material handling equipment;

Council and City Council mean the Council of the City of Kingston;

Downtown Kingston Business Improvement Area means the geographical area as defned in Schedule E to this bylaw.

Emergency means a situation or an impending situation, often dangerous, caused by the forces of nature, an accident, an intentional act or otherwise, which arises suddenly and calls for prompt action;

Emergency vehicle includes a land ambulance, an air ambulance, a fre department vehicle, a police vehicle, and a motor vehicle being used to respond to an emergency;

Explosives Act means the Explosives Act, R.S.C. 1985, c. E-17, as amended, or any successor legislation thereof;

Explosives Regulations means the Explosives Regulations, 2013, SOR/2013-211, as amended, or any successor legislation thereof;

Fireworks means, in the context of this bylaw, consumer freworks as classifed by the Chief Inspector of Explosives in accordance with the Explosives Act and the Explosives Regulations. It also means display freworks and special efect pyrotechnics, as classifed by the Chief Inspector of Explosives in accordance with the Explosives Act and the Explosives Regulations, when the detonation of such has been authorized by the Chief Fire Oficial;

Licensing and Enforcement Division means the administrative unit of the Planning, Building and Licensing Services Department that is responsible for enforcing the general bylaws of the City or, in the event of organizational changes, another administrative unit designated by Council to carry out this responsibility;

Manager of Licensing and Enforcement means the Manager of the Licensing and Enforcement Division, of the Planning, Building and Licensing Services Department, his or her designate or, in the event of organizational changes, another employee designated by City Council.

Motor vehicle includes an automobile, bus, truck, motorcycle, motor assisted bicycle and any other vehicle propelled or driven other than by muscular power, but does not include a motorized snow vehicle, traction engine, farm tractor, other farm vehicle or road-building machine;

Municipal service vehicle means a vehicle operated by or on behalf of the City or a local board of the City while the vehicle is being used for the construction, repair or maintenance of a highway, including the clearing and removal of snow, the construction, repair or maintenance of a utility, the collection or transportation of waste, or other municipal purpose;

Noise means sound that is unusual or excessive, or that is unwanted by or disturbing to persons;

Other areas means the lands designated in Schedule D as “other areas”;

Penalty Notice means a notice given pursuant to sections 2.2 and 2.4 of "Bylaw 2020-69 of the Corporation of the City of Kingston being “A Bylaw to Establish a Process for Administrative Penalties”

Person includes a corporation as well as an individual, and shall include the owner of a property;

Premises means a piece of land and any buildings and structures on it, and includes a place of business, a public highway, private road, lane, pathway and sidewalk, and any other location or place;

Residence means a room, suite of rooms, or dwelling, including a mobile trailer, operated as a housekeeping unit that is used or intended to be used as a separate domicile by one or more persons, and that normally contains cooking, eating, living, sleeping and sanitary facilities;

Residential areas means all lands within the geographic boundaries of the City except for those lands designated in Schedule D as “other areas”;

Sports feld means any area, not on property with a residential use, or vacant and eligible for a residential use, as defned in the City’s zoning bylaws, whether or not delineated by lines, that is designated as a playing surface, and includes any adjacent seating area or stands;

Statutory holiday includes Boxing Day and any day within the defnition of “holiday” in the Retail Business Holidays Act R.S.O. 1990, Ch. R.30, as amended, or any successor thereof;

Utility means a system that is used to provide a utility service to the public, including water,sewage, electricity, gas, communications networks and cable services;

Utility service vehicle means a vehicle operated by or on behalf of Utilities Kingston, its subsidiary companies, and by any other company or agency that supplies or manages a utility within the City while the vehicle is being used for the construction, repair or maintenance of that utility;

Vehicle includes a motor vehicle, trailer, traction engine, farm tractor, road-building machine and other vehicle propelled or driven other than by muscular power; and

Zoning bylaw means a bylaw passed under section 34 of the Planning Act that restricts the use of land.

Part 2 - Application
2.1 The general prohibitions on activities described in Schedule A apply to the lands within the residential areas and other areas of the City designated in Schedule D at all times.

2.2 The prohibitions on activities by time and place described in Schedule B apply to the lands within the residential areas and other areas of the City designated in Schedule D during the days and between the hours specifed in Schedule B.

Part 3 - Administration
3.1 The Licensing and Enforcement Division is responsible for the administration of this bylaw.

3.2 All Provincial Ofences Oficers with authority to enforce the bylaws of the City are responsible for enforcing the provisions of this bylaw.

3.3 Any person may submit an application to the Licensing and Enforcement Division requesting an exemption from any of the prohibitions described in Schedules A and B.

3.4 Council approved exemptions will be in efect for the dates specifed, and Council may impose any conditions that it considers appropriate.

3.5 A Council approved exemption shall be invalid if these conditions are contravened.

3.6 Notwithstanding sections 3.3 and 3.4, the Manager of Licensing and Enforcement, or his or her designate, has delegated authority to approve an application for exemption from the noise prohibitions listed in section 1 and section 3 of Schedule B of this bylaw to permit the pouring, saw-cutting and fnishing of concrete, between 1900 hours and 2300 hours, one day per week, excluding Sundays and Statutory Holidays.

3.7 Notwithstanding sections 3.3 and 3.4, the Manager of Licensing and Enforcement, or his or her designate, has delegated authority to approve an application for exemption from the noise prohibitions listed in section 1 and section 3 of Schedule B of this bylaw to permit construction activity and the operation of construction equipment in connection with construction between 1900 hours and 2100 hours, one day per week, excluding Saturdays, Sundays and Statutory Holidays.

3.8 Exemptions approved by the Manager of Licensing and Enforcement shall be in efect for the dates specifed, and the Manager of Licensing and Enforcement may impose any conditions that he or she considers appropriate.

3.9 An exemption approved by the Manager of Licensing and Enforcement shall be invalid if these conditions are contravened.

Part 4 - Regulations
4.1 No person shall, at any time, make, cause or permit the making noise within the City that is the result of any of the described in Schedule A and that is audible to:

a person in a premises or a vehicle other than the or vehicle from which the noise is originating; or

a person in a residence other than the residence from the noise is originating.

4.2 No person shall, during the days and between the hours specifed in Schedule B, make, cause or permit the making of noise within the residential areas and other areas designated in Schedule D that is the result of any of the activities described in Schedule B and that is audible to:

a person in a premises or a vehicle other than the premises or vehicle from which the noise is originating; or

a person in a residence other than the residence from which the noise is originating.

4.3 No person shall obstruct or hinder or attempt to obstruct or hinder a Provincial Ofences Oficer or other authorized employee or agent of the City in the exercise of a power or the performance of a duty under this bylaw.

4.4 Where a Provincial Ofences Oficer has reasonable grounds to believe that an ofence under this Bylaw has been committed by a Person, the Provincial Ofences Oficer may require the name, address, and proof of identity of that Person.

4.5 Failure to provide proof of identifcation satisfactory to the Provincial Ofences Oficer when requested to do so pursuant to Section 4.4 of this Bylaw shall constitute obstruction of an Oficer under Section 4.3 of this Bylaw.

Part 5 - Exemptions
5.1 The prohibitions described in Schedules A and B do not apply if the noise is the result of measures undertaken in an emergency for the:

immediate health, safety or welfare of the inhabitants; or

preservation or restoration of property;

the noise is clearly of a longer duration or of a more nature than is reasonably necessary to deal with emergency.

5.2 The prohibitions described in Schedules A and B do not apply the noise is the result of any of the activities described in C.

5.3 The prohibitions described in Schedules A and B do not apply the noise is the result of an activity that has been granted exemption under section 3.4, 3.6, or 3.7.

Part 6 - Schedules
The following schedules are attached to and form part of this bylaw:
• Schedule A -General Noise Prohibitions;

• Schedule B -Noise Prohibitions by Time and Place;

• Schedule C -Exemptions from the Noise Prohibitions; and

• Schedule D -Designated Residential Areas and Other Areas

• Schedule E-Downtown Kingston Business Improvement Area

Part 7 - Ofence And Penalty Provisions
7.1a Every person who contravenes any provision of this Bylaw upon issuance of a Penalty Notice in accordance Administrative Penalty Process Bylaw 2020-69, be liable to to the City an Administrative Penalty in accordance with B of Administrative Penalty Process Bylaw 2020-69.

7.1 Notwithstanding section 7.1a of the Bylaw, every person, than a corporation, who contravenes any provision of this is guilty of an ofence and on conviction is liable to a fne of more than $10,000

for a frst ofence and $25,000 for subsequent ofence, as provided for in subsection 429 (2) © the Municipal Act, 2001, as amended from time to time

7.2 Notwithstanding section 7.1a of this Bylaw, every corporation contravenes any provision of this Bylaw and every oficer director of a corporation who knowingly concurs in contravention is guilty of an ofence and on conviction is liable a fne of not more than $50,000 for a frst ofence and for any subsequent ofence, as provided for in subsections and 429(2) (a) of the Municipal Act, 2001, as amended from to time.

7.3 If this bylaw is contravened and a conviction entered, the court which the conviction has been entered and any court of jurisdiction thereafter may, in addition to any other remedy and any penalty that is imposed, make an order prohibiting continuation or repetition of the ofence by the person convicted.

7.4 If a Person is required to pay an Administrative Penalty under section 7.1a in respect of a contravention of this Bylaw, the Person shall not be charged with an ofence in respect of the same contravention.

7.5 In accordance with Section 351 of the Municipal Act, 2001, as amended from time to time, the treasurer of the City may add unpaid fees, charges and/or fnes issued under this Bylaw to the tax roll and collect them in the same manner as property taxes.

Part 8 - Validity
8.1 If a court of competent jurisdiction declares any provision, or part of a provision, of this bylaw to be invalid, or to be of no and efect, it is the intention of Council in enacting this bylaw each and every provision of this bylaw authorized by law applied and enforced in accordance with its terms to the possible according to law.

Part 9 - Commencement
9.1 This bylaw comes into efect three months after the day that receives third reading and is passed.
"""

WATER_REGULATION_TEXT =  """"
A By-Law to Provide For the Regulation of Water Supply
For The City Of Kingston
Water By-law
Enacted June 20, 2006

Amending By-Laws:

By-Law Number: Date of Passing:

2021-107 July 13, 2021

City of Kingston/Utilities Kingston

April 21, 2006

City of Kingston Water By-Law Number 2006-122

…2

By-Law Number 2006-122
A By-Law To Provide For The Regulation Of Water Supply
For The City Of Kingston
PASSED: June 20, 2006

Whereas under Section 11 of the Municipal Act 2001 a municipality may pass by-laws respecting matters within the sphere of jurisdiction of Public Utilities, and Public Utilities includes a system that is used to provide water services for the public;

And Whereas the Ontario Building Code and the Safe Drinking Water Act authorize the City of Kingston to enact by-laws to protect the drinking water supply;

And Whereas it is essential to the citizens of the City of Kingston to have a reliable,safe supply of drinking water;

Whereas section 434.1(1) of the Municipal Act, 2001, as amended from time to time, provides that a municipality may require a person, subject to such conditions as the municipality considers appropriate, to pay an administrative penalty if the municipality is satisfied that the person has failed to comply with a by-law of the municipality passed under this Act;

(By-Law 2006-122; 2021-107)

Now Therefore the Council of the Corporation of the City of Kingston enacts as follows:

Short Title: Water By-law

By-Law Index:

Part 1 - Definitions:

Part 2 Establishing or Altering a Water Service
2.1 Water Connection/Alteration Permit

2.2 Requirements for permit

2.3 Process for permit

2.4 Extensions and connections

2.5 Capital works

2.6 Water service replacements

2.7 Installation - by City

2.8 Installation - City specifications

2.9 Installation inspection by City

2.10 Installation - access for inspection

2.11 Disconnection of service - temporary

2.12 Disconnection of service – permanent

2.13 Multiple water services – prohibited

2.14 Open looped systems – prohibited

2.15 Hydraulic equipment connection - prohibited

Part 3 - Cross Connections/Backflow Prevention
3.1 Protection from contamination:

3.2 Inspection for cross-connections – access:

3.3 Order to install control device:

3.4 Failure to install - notice - water shut-off

3.5 Additional device on service

3.6 Installation to required standards

3.7 Inspection and testing - paid by Owner

3.8 Failure to test device - notification - water shut-off

3.9 Repair - replacement - by Owner

3.10 Removal of device - permission by City

Part 4 – Inspection and access to property
4.1 Inspection powers

4.2 Reduced water supply

4.3 Entry onto land –discontinue supply

4.4 Access to dwellings

4.5 Entry onto land – notice requirements

4.6 City expenses

Part 5 –Water Meters
5.1 Water to be metered - remedy for violation

5.2 Supply - installation - ownership - replacement

5.3 Restoration of water supply - as soon as practicable

5.4 Charges - meters - Owner to pay

5.5 Every building metered - Operating Authority’s discretion

5.6 Installation to City specifications

5.7 Meter location - Operating Authority to consent to change

5.8 Private meters - Owner responsible

5.9 Reading meter - access

5.10 Valve maintenance - responsibility of Owner

5.11 Leaks must be reported

5.12 Interference with meter not permitted

5.13 Owner responsible to repair piping

5.14 Non-functioning meter - amount of water estimated

5.15 Meter reading supersedes remote device reading

…4

Part 6 – Operation and Maintenance of the Water Distribution System
6.1 Maintenance of water service stub - City

6.2 Maintenance of service extension and private main - Owner

6.3 Operation of water shut-off valve

6.4 Access to water shut-off valves

6.5 Responsibility for protection, water loss, damage

6.6 Responsibility - vacant and unheated premises

6.7 Responsibility - water damage

6.8 Responsibility for frozen pipes - City - Owner

6.9 Conditions on water supply

6.10 Unusual service demands

6.11 Unauthorized operation or interference – offence

6.12 Work on the system

6.13 Shut off- repair

6.14 Damage to water distribution system

Part 7 – External Use of Water
7.1 Regulations – external use of water - June, July, August and September 7.2 Exemptions

Part 8 - Fire Hydrants
8.1 Unauthorized operation of fire hydrant – offence

8.2 Responsibility for hydrant maintenance

8.3 Tampering

8.4 Access

8.5 Private hydrants

8.6 Use of water from hydrants

8.7 Improper use of water from fire service - offence

Part 9 - Prohibitions
9.1 Prohibitions under this by-law

Part 10 - Enforcement
10.1 Fine - for contravention

10.2 Continuation - repetition - prohibited - by order

10.3 Offence - additional - damage to waterworks

10.4 Offence - additional - willful damage

10.5 Offence - additional - injuring waterworks

Part 1 - Definitions:
In this By-law:

“Administrative Penalty” means an administrative penalty administered pursuant to “By-Law 2020-69 of The Corporation of the City of Kingston being "ABy-Law to Establish a Process for Administrative Penalties”;

“building” shall mean a structure supplied with water by the City of Kingston;

“City” shall mean the City of Kingston and its operating authority, Utilities Kingston;

“contractor” shall mean a person, partnership, or corporation who contracts to undertake the execution of work commissioned by the Owner or the City to install or maintain watermains, water services, services, hydrants and other appurtenances;

“cross connection” shall mean any temporary, permanent or potential water connection that may allow backflow of contaminants, pollutants, infectious agents, other material or substance that will change the water quality in the water distribution system and includes without limitation, swivel or changeover devices, removable sections, jumper connections and bypass arrangements;

“drinking water system” has the same meaning as in subsection 2(1) of the Safe Drinking Water Act, 2002;

“exemption permit” shall mean approval by the Operating Authority authorizing the permit holder to water newly laid sod, grass seed or a hydro seeded area in accordance with the terms and conditions set out in the permit;

“external use of water” shall mean the use of water for any purpose outside the walls of any building located at a municipal address;

“inspection” shall mean,

(a) an audit,

(b) physical, visual or other examination,

© survey,

(d) test, or

(e) inquiry;

“in-service” shall mean those parts of the water distribution system that have been approved by the Operating Authority for the provision of potable water and in which potable water is available for use;

“land” shall mean all real property, including buildings or any part of any building and all structures, machinery and fixtures erected or placed upon, in, over, under or affixed to land and in the case of utility service providers and the City of Kingston, all buildings or any part of any building erected or placed upon, in, over, under or affixed to land but shall not include machinery whether fixed or not, nor the foundation on which it rests,works structures other than buildings, substructures, poles, towers, lines, nor any of the

City of Kingston Water By-Law Number 2006-122 …6 …6

things exempted from taxation, nor to any easement or the right, use or occupation or other interest in land not owned by utility service providers or the City of Kingston;

“live tap” shall mean a connection to the water distribution system that is in-service and in which isolation of a part or portion of the water distribution system can not be undertaken;

“municipal easement” shall mean an easement in favour of the City;

“municipal right-of way” shall mean a right-of-way in favour of the City;

“occupant” shall mean any lessee, tenant, Owner, the agent of a lessee, tenant or Owner, or any person in possession of a premise;

“operating authority” shall mean Utilities Kingston (1425445 Ontario Limited);

“other charges” shall mean those charges related to repairs, installations, services rendered, or other expenses, exclusive of charges included in water rates, frontage charges and sewage service rates, payable by the consumer as provided for in this by-law or as directed by City Council;

“owner” shall mean any person, including a corporation, who is the registered owner of the property under consideration including a trustee in whom land is vested, a committee of the estate of a mentally incompetent person, an executor, an administrator or a guardian. The obligations of the Owner under this by-law may not be transferred to a party which is not an Owner;

“Penalty Notice” means a notice given pursuant to sections 2.2 and 2.4 of “By-Law 2020-69 of The Corporation of the City of Kingston being "ABy-Law to Establish a Process for Administrative Penalties”;

“permit holder” shall mean the person to whom a Water Connection/Alteration Permit has been issued, or with whom an agreement has been signed, authorizing the installation, repair, renewal, removal or connection to the water distribution system in accordance with the terms and conditions of the permit or agreement;

“person” shall mean an individual, association, partnership, corporation, municipality,Provincial or Federal agency, or any agent or employee thereof;

“plan of subdivision” shall mean a plan approved by the City that clearly outlines all details that are required to develop a parcel of land into a subdivision with individual parcels;

“potable water” shall mean water that is fit for human consumption;

“private watermain” shall mean a pipe connected to a watermain and installed on private property and from which more than one water service and/or hydrant lateral are connected;

“site plan” shall mean a graphical plan of a proposed development illustrating all the features of the development including dwellings, commercial establishments, roads, and other public or private infrastructure that has been approved by the City pursuant to the Planning Act;

“temporary water service” shall mean:

(a) a pipe installed from the water distribution system by the City, for a City project, and for a specified temporary period of time; or

(b) a pipe installed with the permission of the Operating Authority for construction purposes;

“water connection/alteration permit” shall mean approval by the City of Kingston authorizing the permit holder to connect to the water distribution system in accordance with the terms and conditions set out in the permit;

“water distribution system” shall mean the part of the City’s drinking water system that is used in the distribution, storage or supply of water up to and including the water shut-off valve, and is not part of a treatment system;

“watermain” shall mean every water pipe, except water services and portions of private watermains as herein defined, owned and operated by the City;

“water rates” shall mean rates and charges as defined in the Water and Wastewater Rates and Miscellaneous Charges By-law;

“water meter” shall mean a device supplied by the City to measure the quantity or rate of water flowing through a pipe that is used to supply a building;

“water service” shall mean the portion of a water service pipe from the property line to the water meter location, or for a fire service to the inside of the exterior wall of a structure, i.e. an extension of a water service stub;

“water service stub” shall mean the portion of a water service pipe from a watermain to the water shut-off valve;

“water shut-off valve” shall mean the valve on the water service or private main owned and used by the City to shut off or turn on the water supply from the City’s water distribution system to any building;

“water valve” shall mean the valve used to shut off or turn on the supply of water which forms part of the water distribution system;

“water use analysis” shall mean the installation of a recording device to monitor the flow of water through a water meter over a given period of time;

Part 2 – Establishing or Altering a Water Service
2.1 Water Connection/Alteration Permit
The Owner shall obtain a Water Connection/Alteration Permit prior to the installation, repair, renewal, removal, plugging, capping or disconnection of a private watermain or a water service except where such a water connection has been specifically provided for and approved through the City’s Subdivision or Site Plan Approval process or City watermain rehabilitation project.

2.2 Requirements for permit
Applicants for a Water Connection/Alteration Permit shall complete and submit the appropriate forms, provide the required drawings and information, and pay the stipulated fees or charges to the satisfaction of the City. The installation or disconnection of a private watermain or a water service shall not commence until a Water Connection/Alteration Permit is issued and all required payments have been received.

2.3 Process for a permit
Water Connection/Alteration Permit forms shall be available from the Operating Authority and are to be submitted to the Operating Authority along with any plans or drawings detailing the proposed connection, any other supporting information and required fees as stipulated in the Water and Wastewater Rates and Miscellaneous Charges By-Law. The Operating Authority shall review the proposed alteration/connection proposed and shall impose any condition that is deemed advisable and appropriate to ensure the integrity and safety of the water distribution system and the provision of potable water. Any conditions imposed will be identified in writing forming part of the approved permit and said conditions shall be complied with.

2.4 Extensions and connections
Extensions of and connections to the City’s water distribution system shall only be permitted where they conform to the Official Plan of the City.

2.5 Capital works
New water service connections and water service installations made in association with a capital works project of the City shall be subject to all of the permit requirements of this by-law and to the charges and fees set out in applicable by-laws

2.6 Water service replacements
As part of a watermain rehabilitation project the City shall renew water service stubs on public property at its expense and to its specifications when:

(a) piping is deemed by the Operating Authority to be beyond repair;

(b) the existing pipe material is lead and supplies a single detached residence; or

© the replaced public water service is the same diameter, or a 20 mm diameter service.

Replacement piping shall conform to the specifications of the City. If an Owner requests a larger size, the Owner shall pay the difference in material and labour costs.

2.7 Installation - by City
All water service pipes or private watermains that are to be connected to the drinking water system that require a live tap shall only be installed by the operating authority.

2.8 Installation - City specifications
All water service pipes and private watermains located within City property shall be constructed according to the City’s standards. All water service pipes and private watermains located on private property shall be constructed in accordance with the Ontario Building Code as revised from time to time and in accordance with good practices and shall be approved by the Chief Building Official. Where the Ontario Building Code is silent the City’s specifications shall be applied and shall prevail.

2.9 Installation inspection - by City
All water service pipes and appurtenances installed, including those required by a City Subdivision, Site Plan or Development Agreement must be inspected by the City.

2.10 Installation - access for inspection
The City and persons authorized by the City for inspection shall be, at all times, entitled to enter any premises for the purposes of examining pipes, connections and fixtures which are used in connection with the water service pipe and/or service main.

2. 11 Disconnection of service - temporary
When an Owner temporarily discontinues the use of a water service for water supply to a building, the Owner shall pay to the City a charge as indicated in the Water and Wastewater Rates and Miscellaneous Charges By-Law for disconnecting the water meter for such service from the water distribution system.

2.12 Disconnection of service - permanent
When an owner permanently discontinues the use of a water service or private water watermain for water supply to a building or buildings the water service pipe or private watermain must be disconnected at the watermain, the watermain plugged or capped and the curb box and rod removed at the Owner’s expense. All work must be inspected by the City and the owner shall pay for such inspection as required in the Water and Wastewater Rates and Miscellaneous Charges By-Law.

2.13 Multiple water services -prohibited
Only one water service per lot shall be permitted from the water distribution system. In situations where a shared water service would result from a division of land the shared water service shall be eliminated and a separate water service to each lot from the water distribution system shall be installed at the owners expense.

2.14 Opened loop systems - prohibited
No owner or occupant shall use or cause to be used any type of open loop water system as part of any heating, air conditioning or refrigeration equipment.

2.15 Hydraulic equipment connections - prohibited
No owner or occupant shall connect or permit to be connected to any part of the water system any hydraulic motor, elevator or other type of appliance that operates in whole or in part using potable water.

Part 3 - Cross Connections/Backflow Prevention
3.1 Protection from contamination
No person shall connect, cause to be connected or allow to remain connected to the plumbing system within a building or water distribution system any piping, fixture, fitting container or appliance in a manner which under any circumstances may allow water, waste water, non potable water or any other liquid, chemical or substance to enter the plumbing system within a building or water distribution system. The means for protection from contamination shall be in accordance with the requirements of the Ontario Building Code Act, 1992, as amended from time to time.

3.2 Inspection for cross-connections – access
Any person authorized by the City to conduct an inspection of any component of the drinking water system or its appurtenances, whether privately owned or not has free access at all reasonable times, and upon reasonable notice given in accordance with this By-law, to all parts of every building or other premises to which any water service pipe is supplied for the purpose of inspecting or repairing, or of altering or disconnecting any water service pipe, wire, rod or cross connection within or without the building.

3.3 Order to install control device
If a condition is found to exist which is contrary to Section 3.1 of this By-law, the Operating Authority shall immediately carry out an inspection and shall issue such order or orders to the Owner as may be required to obtain compliance with Section 3.1 of this By-law.

3.4 Failure to install - notice - water shut-off
If the Owner to whom the City has issued an order or notice pursuant to section 3.3, 3.5, 3.7, 3.8 or 3.9 fails to comply with that order or notice, the Operating Authority, at it’s discretion, may:

(a) give notice to the Owner to correct the fault, at his/her expense, within a

specified time period and, if the notice is not complied with, the Operating Authority may then shut off the water service or services; or

(b) shut off the water service or services upon complying with the notice provisions in this by-law.

3.5 Additional device on service
Notwithstanding sections 3.1, 3.3 and 3.4 of this by-law, where a risk of possible contamination of the water distribution system exists in the opinion of the Operating Authority, an Owner shall, on notice from the Operating Authority, install on his/her water service pipe a cross connection control device, approved by the Operating Authority, in addition to any cross connection control devices installed in the Owner’s water system at the source of potential contamination.

3.6 Installation to required standards
Cross connection control or backflow prevention devices, when required by the City,shall be installed in accordance with the Ontario Building Code and “CAN/CSA-B64.10-94 Manual for the Selection, Installation, Maintenance and Field Testing of Backflow Prevention Devices”, as amended from time to time.

3.7 Inspection and testing - paid by Owner
All backflow prevention devices shall be inspected and tested at the expense of the Owner, upon installation, and thereafter annually, or more often if required by the Operating Authority, by personnel approved by the Operating Authority to carry out such tests to demonstrate that the device is in good working condition. The Owner shall submit a report on a form approved by the Operating Authority or any or all tests performed on a cross connection control device within ten (10) days of a test, and a record card shall be displayed on or adjacent to the cross connection control device on which the tester shall record the address of the premises, the location, type,manufacturer, serial number and size of the device, and the test date, the tester’s initials, the tester’s name (if self employed) or the name of his employer and the tester’s license number.

3.8 Failure to test device - notification - water shut-off
If an Owner fails to have a cross connection control device tested, the Operating Authority may notify the Owner that the backflow prevention device must be tested within four (4) days of the Owner receiving the notice.

3.9 Repair - replacement - by Owner
When the results of a test referred to in Section 3.7 of this by-law show that a cross connection control device is not in good working condition, the Owner shall provide written confirmation of the failure to the Operating Authority within twenty-four (24)hours of the test and make repairs or replace the device within four (4) days of the date of the test.

3.10 Removal of device - permission by City
No person shall without the prior written approval of the Operating Authority remove any cross connection control or backflow prevention devices installed as a requirement of provincial legislation or by order under Section 3.3 notwithstanding the fact that the applicable provincial regulation has been rescinded.

Part 4 – Inspection and access to property
4.1 Inspection powers
The Operating Authority or any person designated by it as inspector for purposes of this by-law may, at reasonable times enter onto any land on which the City supplies drinking water for the following purposes:

a) to install, inspect, repair, alter, or disconnect the service pipe or wire,machinery, equipment and other works used to supply drinking water to the building or land;

b) to inspect, install, repair, replace or alter a water meter; or

c) to determine if this by-law, an order, or condition to any permit is being complied with.

4.2 Reduce supply of water
For the purpose of carrying out an installation, inspection, repair, disconnection or other work the City may shut off or reduce the supply of water to any building or land.

4.3 Entry on land – discontinue supply
If an owner discontinues the use of the water supply or the City lawfully decides to cease the supplying water to any building or land, the City may enter onto the premises:

a) to shut off the supply of water

b) to remove any property of the City; or

c) to determine whether the supply of water is being used lawfully

4.4 Access to dwellings
An inspector shall not enter a place being used as a dwelling unless:

a) the consent of the occupier is first obtained, ensuring the occupier is first advised that entry may be denied and in such circumstance, entry can only occur thereafter under authority of a warrant;

b) a warrant under section 158 of the Provincial Offences Act is obtained;

c) the delay necessary to obtain a warrant or the consent of the occupier would result in the immediate danger to the health or safety of any person; or

d) the entry is for the purpose of section 4.1 or 4.3 and the notice provisions of this by-law have been complied with.

4.5 Entry on land – notice requirements
Whenever an inspector exercises a power of entry pursuant to this By-law, the inspector shall:

a) provide reasonable notice of the proposed entry to the occupier of the land by personal service or prepaid mail or by posting the notice on the land in a conspicuous place for three consecutive days prior to entry;

b) where the proposed entry is an inspection authorized by sections 4.1 or 4.3,the inspector must provide reasonable notice by means of personal service only;

c) in so far as is practicable, restore the land to its original condition where any damage is caused by the inspection; and

d) provide compensation for any damage caused and not remedied.

4.6 City expenses
All costs incurred by the City to perform work required by this by-law shall be charged to the Owner of the property where such work is performed and shall be collected according to law, and until paid, such cost shall remain a lien on such property, and may also be collected in the like manner as taxes. The City shall not be held responsible for the cost of restoration.

Part 5 –Water Meters
5.1 Water to be metered - remedy for violation
All water drawn from the water distribution systems, except water used for fire fighting purposes, or water use authorized by the Operating Authority, shall pass through the water meter supplied by the City for use upon such premises, and in addition to whatever other remedies the City may have by law in respect to infringement of this by-law, the City may, upon ascertaining that water has been used which has not passed through the water meter of such premises, shut off and stop the supply of water upon providing notice as required by this By-law.

5.2 Supply - installation - ownership - replacement
The Owner shall pay the water service installation charge as indicated in the Water and Waste Water Rates and Miscellaneous Charges By-Law as amended from time to time,before the City will supply the Owner with a water meter and the water meter must be installed prior to occupancy of the building. The water meter shall remain the exclusive property of the City and may be removed as and when the City may see fit, upon the same being replaced by another water meter, or for any reason which the City may, in its discretion, deem sufficient.

5.3 Restoration of water supply - as soon as practicable
If the City has shut off or restricted the supply of water under section 4.2 of this by-law,the City shall restore the supply of water as soon as practicable upon completion of the required work.

5.4 Charges - meters - owner to pay
Charges for all measured water consumption, as well as any work or services performed by the Operating Authority will be determined by the Operating Authority as indicated in the Water and Waste Water Rates and Miscellaneous Charges By-Law as amended from time to time and will be paid in full by the Owner. Work performed on the water distribution system that requires an owner or occupant to flush their plumbing system within the building to remove dirt or cloudiness shall not be exempt in part or in whole from any measured water consumption and the applicable rates or charges.

5.5 Every building metered - Operating Authority’s discretion
Every building or property shall be water metered at the absolute sole discretion of the Operating Authority.

5.6 Installation to City specifications
All water meters, supplied by the City, shall be installed to conform to the specifications of the City.

5.7 Meter location - Operating Authority to consent to change
The location of a water meter, once installed to the specifications of the City, shall not be changed by any person except with the consent of the Operating Authority.

5.8 Private meters - Owner responsible
The City will not supply, install, inspect or read private water meters, nor will the City bill consumption on private water meters. Water supply pipes to private water meters shall only be connected to the owner’s plumbing on the outlet side of the City’s water meter.

5.9 Reading meter - access
The City and persons authorized by the City shall be allowed access to the premises and be provided free and clear access to the water meter where water is being supplied at all reasonable times for the purpose of reading, at the discretion of the City. Where such access to the premises and/or free and clear access to a water meter is not provided by the Owner within fourteen (14) days upon notification as required by this By-law, the City may, at its discretion, shut off the supply of water to the premises until such time as free and clear access to the water meter is provided.

5.10 Valve maintenance - responsibility of Owner
The Owner shall supply, install and be responsible for maintaining in good working order the inlet valve to the water meter, the outlet and bypass valves for all water meters, and shall ensure that such valving is accessible.

5.11 Leaks must be reported
Any leaks that develop at the water meter or its couplings must be reported immediately to the Operating Authority. The City is not liable for damage caused by such leaks.

5.12 Interference with meter not permitted
No person, other than persons authorized by the Operating Authority for that purpose shall be permitted to open, or in any way whatsoever to tamper with any water meter, or with the seals placed thereon, or do any manner of thing which may interfere with the proper registration of the quantity of water passing through such water meter, and should any person change, tamper with or otherwise interfere, in any way whatsoever,with any water meter placed in any building, the Operating Authority may shut off the water from such building or premises, and the water shall not be again turned on to such building or premises without the express consent of the Operating Authority.

5.13 Owner responsible to repair piping
If, in the opinion of the Operating Authority, the condition of the water service pipe and/or valves and the plumbing system on such piping is such that the water meter cannot be safely removed for the purpose of testing, replacing, repairing or testing in place without fear of damage to the water service pipe and valves, the Operating Authority may require the Owner to make such repairs as may be deemed necessary to facilitate the removal or testing of the water meter. If, upon notification, the Owner does not comply with the Operating Authority’s request, then the water supply to the property may be turned off at the shut-off valve during removal, replacement, repair and testing of the water meter and the City shall not be held responsible for any damages to the Owner’s property arising from such work.

5.14 Non-functioning meter - amount of water estimated
If, for any cause, any water meter shall be found to not be working properly, then the amount of water to be charged for shall be estimated on the average reading for the previous months, when the water meter was working properly, or, if unavailable or proven inaccurate, the amount of water to be charged for shall be estimated on a daily average when the water meter is working properly, and the charge for the water for the period during which the water meter was not working properly shall be based thereon.

5.15 Meter reading supersedes remote device reading
Where the water meter is equipped with a remote read-out unit of any type and a discrepancy occurs between the reading at the register of the water meter itself and the reading on the readout device, the City will consider the reading at the water meter to be correct, and will adjust and correct the Owner’s account accordingly.

Part 6 – Operation and Maintenance of the Water Distribution System
6.1 Maintenance of water service stub - City
The water service stub shall be maintained by the City at the City’s expense.

6.2 Maintenance of service extension and private watermain - Owner
Any and all defects, including the breaking of a water service, private watermain and meter pit shall be repaired by the Owner of the property being serviced. Should the City become aware of any such defect, and upon written notification to the Owner, the said defect is not repaired within seven (7) days of the date of the notification or within such time as the Operating Authority may deem necessary, then the City may turn off the water supply to the property. If the City is ordered to restore the water supply, then the City may repair the defective water service pipe.

6.3 Operation of water shut-off valve
No person, other than persons authorized by the Operating Authority for that purpose shall be permitted to operate the water shut-off valve to any premises.

6.4 Access to water shut-off valves
All water shut-off valves must be left clear and accessible at all times so that the water in the water service pipe and private watermains may be turned off or on as may be found necessary by the Operating Authority.

6.5 Responsibility for protection, water loss, damage
All water service to and including the water meter shall be properly protected from frost and any other damage at the expense and risk of the Owner of the property being serviced. The Owner shall be responsible for the water loss occasioned by a leak in the water service and/or private main and the charge for such water loss shall be determined by the Operating Authority, shall be paid by the Owner upon demand by the City, and the City shall not be held responsible for any damages arising from such leakage.

6.6 Responsibility - vacant and unheated premises
When any premises is left vacant or without heat it is the Owner’s responsibility to shut off the water supply from within the premises and to drain the piping therein. The Owner shall request that the Operating Authority have the water shut-off valve turned off to stop the water supply. The valve will be turned on only at the Owner’s request and in the Owner’s presence. The Owner shall pay for this service at the rate as indicated in the Water and Wastewater Rates and Miscellaneous Charges By-Law

6.7 Responsibility - water damage
When any premises left vacant, unattended or without heat, where the water supply has not been shut off, suffers damage to it and its contents from a leaking or burst water pipe, the Owner or Occupant shall have no claim against the City.

6.8 Responsibility for frozen pipes - City - Owner
Thawing out frozen water service stubs shall be the City’s responsibility. Thawing out a frozen water service or private watermains shall be the Owner’s responsibility. Where any employee of the City assists the Owner in the thawing of frozen pipes on the Owner’s property, all such assistance work will be considered to be at the Owner’s risk, and the Owner shall have no claim against the City by reason of such work.

6.9 Conditions on water supply
The City agrees to use reasonable diligence in providing a regular and uninterrupted supply and quality of water, but does not guarantee a constant service or the maintenance of unvaried pressure or quality or supply of water and is not liable for damages to the Owner or Occupant caused by the breaking of any water service pipe or attachment, or for the shutting off of water to repair or rehabilitate watermains or to tap watermains. Where planned work on the water distribution is contemplated the Operating Authority will make reasonable effort to provide two (2) days notice, delivered to the lands affected, of the intention to shut off the water, save and except for emergency shut downs.

6.10 Unusual service demands
Where an Owner requires a supply, a guaranteed supply or quality of water or water pressures beyond that provided by the water distribution system, the Owner is responsible for providing such services, devices or processes that satisfy their specific requirements.

6.11 Unauthorized operation or interference – offence
No person, other than persons authorized by the Operating Authority for that purpose shall open or close a water valve in the public water distribution system, or remove,tamper with or in any way interfere with any water shut-off valve, water meter, structure,watermain or water service in the water distribution system, including private watermains, nor tap off or make any connection to a watermain.

6.12 Work on the system
The City shall perform all work having to do with the City’s water distribution system and with the installation, repair, renewal, or removal of the City’s in-service water distribution system. The Operating Authority may delegate to any person the authority to perform work on the water distribution system, on conditions acceptable to the Operating Authority.

6.13 Shut off- repair
The City shall have the right at any time and without notice to shut off the supply of water to any building if, in the opinion of the Operating Authority, the water service located on the property is not being properly maintained, develops a significant leak, or in any way compromises the integrity of the City’s water works, and not to restore service until such condition has been rectified to the satisfaction of the Operating Authority.

6.14 Damage to water distribution system – offence
No person shall break, damage, destroy, deface or tamper with, or cause or permit the breaking, damaging, destroying, defacing or tampering with any part of the water distribution system.

Part 7 – External Use of Water
7.1 Regulations – external use of water - June, July, August and September The following restrictions on the use of water outside of any building are effective within all areas of the City serviced by the water distribution system:

(a) During the period from June 15th to September 15th, the external use of water is permitted:

(i) on even calendar dates at only those municipal addresses ending with numbers 0, 2, 4, 6, 8;

(ii) on odd calendar dates at only those municipal addresses ending with numbers 1, 3, 5, 7, 9;

(iii) only between the hours of 5:00 a.m. and 10:00 a.m. on the day permitted for the external use of water where a lawn sprinkler or similar device is used.

(b) The Operating Authority, in its absolute discretion, is authorized to impose at any time any other water use regulation which it deems advisable to further limit the external use of water. This authority shall include, but is not limited to, the right to further limit the hours of external water use on permitted days and to ban completely the external use of water at any time.

© Notice of an additional water use regulation and the effective date thereof shall be given by the Operating Authority by publishing in a newspaper of local circulation notice of the additional water use regulations on three (3) consecutive days.

(d) Following the notice of an additional water use regulation, no person shall use water except in accordance with the provisions of such regulation.

7.2 Exemptions
a) Any person may, from a water source other than the municipal water distribution system, use water externally.

(b) The Operating Authority may, in its sole discretion, exempt any property or portion thereof from Section 7.1 by issuing an exemption permit.

© The person requesting the exemption must submit a written application in a form approved by the Operating Authority and pay a fee of fifty-five dollars ($55.00) per exemption per property.

(d) Any exemption permit issued pursuant to section 7.2(b) shall be deemed to contain the following conditions:

(i) New sod, grass seed, or hydro seeded areas may be watered using a sprinkler or other similar device between the hours of 5 a.m. and 10 a.m. for seven (7) consecutive days commencing on the date specified in the exemption permit;

(ii) New trees or shrubs may be watered by a hand held hose only between the hours of 5 a.m. and 10 a.m. for seven (7) consecutive days commencing on the date specified in the exemption permit;

(iii) For circumstances where complying with section 7.1 would cause irreparable damage or impose undue hardship on a property owner the Operating Authority may issue an exemption permit to permit watering of any property between the hours of 5 a.m. and 10 a.m. for up to seven (7) consecutive days commencing on the date specified in the exemption permit;

(iv) The exemption permit shall be posted in a conspicuous place on the property for which the exemption permit applies; and

(v) No more than one (1) exemption permit may be issued per property per year.

(e) Notwithstanding any other provision of this by-law, the Operating Authority may permit up to two (2), seven (7) consecutive day extensions pursuant to section 7.2(d)(iii) per year, per property provided that the applicant pays a separate fee for each seven (7) day extension.

Part 8 - Fire Hydrants
8.1 Unauthorized operation of fire hydrant – offence
No person, except for city personnel authorized under the Safe Drinking Water Act,2002, is permitted to operate a fire hydrant.

8.2 Responsibility for hydrant maintenance
Any hydrant situated within the road allowance is the property of the City and shall be maintained by it; City-owned hydrants located on private property shall be maintained by the City. Hydrants owned and paid for by any persons other than the City shall be maintained by such persons.

8.3. Tampering
No person shall paint fire hydrants or tamper with the colour scheme of fire hydrants except with the permission of the Operating Authority.

8.4. Access
No person shall obstruct the free access to any fire hydrant or plant or place, or cause or permit to be planted or placed, vegetation or other objects within a 3 metre corridor between the hydrant and the curb nor within a 1.5 metre radius beside or behind a hydrant except with the prior written authorization of the Operating Authority.

8.5. Private hydrants
Private hydrants shall be maintained accessible at all times and in good operating condition by and at the expense of the Owner and shall be tested on a regular basis at the Owner’s expense and in accordance with the Ontario Fire Code.

8.6. Use of water from hydrants
Except for water used for fire fighting and those operations as authorized by the Operating Authority, any other use of a City’s fire hydrant for water supply is prohibited.

8.7. Improper use of water from fire service - offence
Any water supplied or made available for any land or building for purposes of protection of property or persons from fire or for preventing fires or the spreading of fires shall not be used for any other purpose.

Part 9 - Prohibitions
9.1 Prohibitions under this by-law
No person shall:
(a) contravene any provision of this by-law or any order or notice issued pursuant to this by-law;

(b) hinder or interrupt, or cause or procure to be hindered or interrupted, the corporation or any of its officers, contractors, agents, servants or workers, in the exercise of any of the power conferred by this by-law;

© let off or discharge water so that the water runs waste or useless out of the works;

(d) improperly waste the water or, without the consent of the City, lend, sell, or dispose of the water, give it away, permit it to be taken or carried away, use or apply it to the use or benefit of another, or to any use and benefit other than his own or increase the supply of water agreed for;

(e) without lawful authority open or close any valve or hydrant, or obstruct the free access to any hydrant, stopcock, valve, chamber or pipe by placing on it any building material, rubbish or other obstruction;

(f) throw or deposit any injurious or offensive matter into the water or waterworks,or upon the ice if the water is frozen, or in any way foul the water or commit any damage or injury to the works, pipes or water, or encourage the same to be done;

(g) alter any water meter placed upon any service pipe or connected therewith, within or without any building or other place, so as to lessen or alter the amount of water registered; or

(h) lay or cause to be laid any pipe or watermain to connect with any pipe or watermain of the water distribution system, or in any way obtain or use the water without the consent of the corporation

(i) use or permit the use of water externally except in accordance with the regulations specifically set out in this by-law and any other regulation imposed by the Operating Authority.

Part 10 - Enforcement
10.1a Every Person who contravenes any provision of this By-Law shall, upon issuance of a Penalty Notice in accordance with Administrative Penalty Process By-Law 2020-69, be liable to pay to the City an Administrative Penalty as set out in Schedule B of the Administrative Penalty Process By-Law.

(By-Law 2006-122; 2021-107)

10.1 Fine - for contravention
Notwithstanding Part 10.1a of this By-Law, any person who contravenes any provision of this by-law is, upon conviction, guilty of an offence and is liable to any penalty as provided in the Provincial Offences Act.

(By-Law 2006-122; 2021-107)

10.2 Continuation - repetition - prohibited - by order
The court in which the conviction has been entered, and any court of competent jurisdiction thereafter, may make an order prohibiting the continuation or repetition of the offence by the person convicted, and such order shall be in addition to any other penalty imposed on the person convicted.

10.3 Offence - additional - damage to waterworks
Every person who, by act, default, neglect or omission occasions any loss, damage or injury to any water public utility works, or to any waterworks plant, machinery, fitting or appurtenance thereof is liable to the City for all damages caused.

10.4 Offence - additional - willful damage
Every person who damages or causes or permits to be damaged any water meter,water service pipe, conduit, wire, rod or water fitting belonging to the City or impairs or causes or permits the same to be altered or impaired, so that the water meter indicates less than the actual amount of the water that passes through it, is guilty of an offence and on conviction is liable to a fine, to the use of the City, and for any expenses of repairing or replacing the water meter, water service pipe, conduit, wire, rod or fitting all of which is recoverable under the Provincial Offences Act.

10.5 Offence - additional - injuring waterworks
Every person who removes, destroys, damages, alters or in any way injures any water service pipe, conduit, wire, rod, pedestal, post, plug, lamp or other apparatus or thing belonging to the City is guilty of an offence and on conviction is liable to a fine, to the use of the City, and is also liable for all damages occasioned thereby, which are recoverable under the Provincial Offences Act.

10.6 Where an Officer has reasonable grounds to believe that an offence under this By-Law has been committed by a Person, the Officer may require the name, address,and proof of identity of that Person.

10.7 If a Person is required to pay an Administrative Penalty under section 10.1a in respect of a contravention of this By-Law, the Person shall not be charged with an offence in respect of the same contravention.

City of Kingston Water By-Law Number 2006-122

…22

10.8 In accordance with section 351 of the Municipal Act, 2001, as amended from time to time, the treasurer of the City may add unpaid fees, charges and/or fines issued under this By-Law to the tax roll and collect them in the same manner as property taxes.

(By-Law 2006-122; 2021-107)

In the event any provision, or part thereof, of this By-law is found by a court of competent jurisdiction to be ultra vires, such provision, or part thereof, shall be determined to be severed, and the remaining portion of such provision and all other provisions of this by-law shall remain in full force and effect.

This By-law shall come into full force and effect on the date of its passing.
"""

TREE_BYLAW_TEXT = """Corporation Of The City Of Kingston
Ontario
By-Law Number 2018-15

Being a By-Law to Prohibit and Regulate the Destruction or Injuring

of Trees in the City of Kingston, and to Repeal and Replace

By-Law Number 2007-170, as amended

(Short Title, “Tree By-Law”)

Passed: December 19, 2017

As Amended By:

By-Law Number: Date Passed:

By-law Number 2021-111 July 13, 2021

City of Kingston By-Law Number 2018-15, “Tree By-Law”

Page 2 of 23

By-Law Number 2018-15
Being a By-Law to Prohibit and Regulate the Destruction or Injuring
of Trees in the City of Kingston, and to Repeal and Replace

By-Law Number 2007-170, as amended

Passed: December 19, 2017

Whereas Section 135(1) of the Municipal Act, 2001, SO 2001, c. 25, permits the enactment of a by-law by the Council of The Corporation of the City of Kingston to prohibit or regulate the destruction or injuring of trees; and

Whereas Council may also require that a permit be obtained for the injury or destruction of trees within the City of Kingston, and may prescribe the fees for the permit, the circumstances under which a permit may be issued, and the conditions to such a permit; and

Whereas Council deems it to be desirable to enact a Tree By-Law for the purposes of:

(a) Regulating and controlling the removal, maintenance, and protection of trees and woodlands.

(b) Controlling the clear cutting of trees.

© Supporting the City’s Strategic Plan and the goal of intensifying the city’s urban forest.

(d) Achieving the objectives of the city’s Official Plan by sustaining a healthy, natural environment.

(e) Protecting and enhancing the biodiversity of woodlands, wildlife habitat, and related ecological functions.

(f) Promoting Good Forestry Practices and Good Arboricultural Practices that sustain healthy woodlands and tree coverage.

(g) Contributing to human health and quality of life.

(h) Mitigating greenhouse gas emissions and reducing the effects of climate change.

Whereas section 434.1(1) of the Municipal Act, 2001, as amended from time to time, provides that a municipality may require a person, subject to such conditions as the municipality considers appropriate, to pay an administrative penalty if the municipality is satisfied that the person has failed to comply with a by-law of the municipality passed under this Act;

Therefore be it resolved that the Council of The Corporation of the City of Kingston hereby enacts as follows:

Definitions
1. In this by-law, the following definitions apply:
(1) “Administrative Penalty” means an administrative penalty administered pursuant to “By-Law 2020-69 of The Corporation of the City of Kingston being"ABy-Law to Establish a Process for Administrative Penalties

(2) “Agricultural Operation” means land used for the commercial production of crops or raising of livestock and includes cultivation, seeding, and harvesting.

(3) “Applicant” means a person who submits an application to the city for a Tree Permit pursuant to the provisions of this by-law.

(4) “Building Permit” means a Building Permit issued pursuant to the Building Code Act, 1992, SO 1992, c. 23.

(5) “Certified Arborist” means an arborist certified by the Certification Board of the International Society of Arboriculture.

(6) “Certified Tree Marker” means an individual who has full certification, and is in good standing, under the Ontario Ministry of Natural Resources and Forestry program for marking Trees.

(7) “City” means The Corporation of the City of Kingston.

(8) “Clear Cutting” means the removal of all Trees within a portion of a Woodland or a Significant Woodland where the area to be cleared is in excess of 0.2 hectare.

(9) “Closure Plan means a plan that outlines how the affected land will be rehabilitated and the costs associated with doing so with respect to the Mining Act.

(10) “Commercial Harvesting” means the business of felling Trees and transporting logs to a market, with the expectation of financial gain or reward.

(11) “Cord” means a pile of healthy, live wood that when stacked, measures 3.63 cubic metres (128 cubic feet) in volume.

(12) “Dead Tree” means a Tree that has no living tissue as determined by a Qualified Person.

Page 4 of 23

(13) “Designate” means a person who is an employee of the city and who has been appointed by the Director to administer all or part of this By-Law on behalf of the Director.

(14) “Destroy” or “Destruction” means any act that renders, or which is likely to render, a Tree unviable or compromise its life processes in such a way that it cannot survive.

(15) “Diameter at Breast Height” (“DBH”) means the diameter of the trunk of a Tree measured in centimetres outside the bark at a point that is 1.37 metres above the ground.

(16) “Director” means the Director of Planning, Building and Licensing Services or any successor position, and includes his or her Designate.

(17) “Diseased Tree means a sustained and progressive impairment of the structure or function of a Tree. Symptoms may include dieback, foliage discoloration, decay, galls, or wilting.

(18) “Distinctive Tree” means a healthy Tree that is considered by the Director to be an uncommon species in the City of Kingston region and environment, or a Tree of an uncommon size, maturity or age, and includes, without limitation, those Tree species listed in Schedule ‘A’ to this By-Law.

(19) “Ecological Function” means the natural processes, products or services that living and non-living environments provide or perform within or between species, ecosystems and landscapes. These may include biological, physical and socio-economic interactions.

(20) “Emergency Work” means any work required to be carried out immediately in order to prevent imminent danger to life, health or property from natural events (including lightning, wind, hail or an extreme snow event) or unforeseen circumstances (i.e. automobile accidents), and includes work of an urgent nature which can be associated with drain repairs, utility repairs or structural repairs to a building, and work required to prevent soil erosion, slipping of soil or damage to Trees.

(21) “Environmental Impact Assessment” (“EIA”) means an analysis performed by a Qualified Person with current knowledge in the field of biology, ecology, hydrology or other specialty as required by specific circumstances that inventories and assesses the potential impact of a development on Natural Heritage Features and Areas, and their Ecological Function and makes recommendations for measures to ensure that the proposed development has no Negative Impacts on those features and areas and their Ecological Functions.

City of Kingston By-Law Number 2018-15, “Tree By-Law”
Page 5 of 23

(22) “Environmental Protection Areas” means areas of natural and scientific interest (ANSIs), fish habitat or significant wildlife habitat areas, provincially significant wetlands, significant coastal wetlands and locally significant wetlands, rivers, streams and small inland lake systems and the Snake and Salmon Islands, located in Lake Ontario, all of which are shown in the City of Kingston Official Plan.

(23) “Forest Management Plan” means a document, including prescriptions for Silviculture and ecological conservation, prepared by a Registered Professional Forester on behalf of an Owner for the purpose of managing natural and forestry resources in accordance with Good Forestry Practices.

(24) “Good Arboricultural Practice” means the proper planting and care of Trees in accordance with the standards set by the International Society of Arboriculture.

(25) “Good Forestry Practice” means the proper implementation of harvest,renewal, and maintenance activities known to be appropriate for forest and environmental conditions under which they are being applied that minimize detriments to forest values, including significant ecosystems, important fish and wildlife habitat, soil and water quality and quantity, forest productivity and health;

(26) “Hazard Tree” means a Tree that is severely damaged to the extent that it poses an immediate safety threat to Persons or property.

(27) “Injure” or “Injury” means any action that causes physical, biological, or chemical harm or damage to a Tree.

(28) “Landscaping, Replanting and Replacement Plan” means a plan which identifies the number, location, species and size of existing Trees, Trees to be planted or replaced and other landscaping elements on a property and provides details regarding planting methodology and timing.

(29) “Natural Heritage Features and Areas” means features and areas, including significant wetlands, significant coastal wetlands, other coastal wetlands, fish habitat, waters supporting aquatic species at risk, Significant Woodlands, significant valleylands, significant habitat of endangered species and threatened species, significant wildlife habitat, and significant areas of natural and scientific interest, which are important for their environmental and social values as a legacy of the natural landscapes of an area.

(30) “Negative Impacts” means in regards to Natural Heritage Features and Areas, degradation that threatens the health and integrity of the natural features or Ecological Functions for which an area is identified due to single, multiple or successive development or Site Alteration activities.

City of Kingston By-Law Number 2018-15, “Tree By-Law”
Page 6 of 23
(31) “Normal Farm Practice” means a practice, as defined in the Farming and Food Production Protection Act, 1998, SO 1998, c. 1, that is conducted in a manner consistent with proper and acceptable customs and standards as established and followed by similar agricultural operations under similar circumstances or a practice which makes use of innovative technology in a manner consistent with proper advanced farm management practices.

(32) “Officer” means an individual appointed by the City to enforce the provisions of this By-Law, and includes a municipal by-law enforcement officer.

(33) “Official Plan” means the City of Kingston Official Plan, being a land use document that sets out the goals, objectives and policies established primarily to manage and direct physical change and the effects of such change on the social, economic and natural environment of the municipality.

(34) “Open Space” means areas in the municipality designated Open Space in the City of Kingston Official Plan, which include public parks, private open space areas, and natural reserves.

(35) “Owner” means the Person(s) registered on the title of the land in the Land Registry Office.

(36) “Penalty Notice” means a notice given pursuant to sections 2.2 and 2.4 of “By-law 2020-69 of The Corporation of the City of Kingston being"ABy-Law to Establish a Process for Administrative Penalties.

(37) “Person” means an individual, firm, corporation, association or partnership.

(38) “Personal Use” means the utilization of a Tree, Trees or Tree sections Destroyed or Injured and collected solely for the Owner’s use (e.g. fuel wood) and includes the accessory sale of no more than three (3) Cords of wood within a consecutive period of twelve (12) months.

(39) “Pruning” means the removal, as appropriate, of not more than one-third of the live branches or limbs of a tree in accordance with Good Arboricultural Practice.

(40) “Plant Nursery” means the use of land, buildings or structures, or portions thereof, where Trees, shrubs or other plants are grown for the purpose of retail or wholesale trade. A Plant Nursery may include the accessory sale of soil, planting materials, fertilizers, garden equipment, ornaments and similar material.

Page 7 of 23

(41) “Qualified Person” means an individual with qualifications and/or credentials related to a field of study and who is therefore appropriate for conducting a study and/or providing an expert opinion that has been required by the City. The qualifications and credentials of the Qualified Person must be to the satisfaction of the City, or where appropriate, may be defined by relevant legislation, regulations and standards.

(42) “Registered Professional Forester” means a member of the Ontario Professional Foresters Association as defined in the Professional Foresters Act, 2000, SO 2000, c. 18.

(43) “Residential Unit” means a unit that consists of a self-contained set of rooms located in a building or structure, used or intended for use as a residential premises and contains a kitchen and bathroom facilities that are exclusive to the users of the unit.

(44) “Rural Area” means the area located outside of the Urban Boundary, as shown in the City of Kingston Official Plan as indicated in Schedule ‘B’ of this By-Law.

(45) “Selective harvesting” means the selective removal of trees, undertaken in accordance with Good Arboricultural Practices and Good Forestry Practices, that allows for regrowth and does not result in Clear Cutting”.

(46) “Significant Woodlands” means an area shown in the City of Kingston Official Plan and indicated on Schedule ‘C’ of this By-Law. Significant Woodlands have been identified through the Central Cataraqui Region Natural Heritage Study (2006) or identified using criteria established by the Ontario Ministry of Natural Resources and Forestry which are ecologically important in terms of features such as species composition, age of trees and stand history; functionally important due to its contribution to the broader landscape because of its location, size or the amount of forest cover in the planning area; or economically important due to site quality, species composition, or past forest management history.

(47) “Silviculture” means the theory and practice of growing and cultivating trees to achieve the objectives of forest management.

(48) “Silvicultural Prescription” means the site specific operational plan, signed and sealed by a Certified Arborist that describes the existing forest conditions and the forest management objectives for an area, and which prescribes the methods for harvesting the existing forest stand and a series of silvicultural treatments that will be carried out to establish a free-growing stand in a manner that accommodates other resource values as identified.

(49) “Site Alteration” means activities, such as grading, excavation and the placement of fill that change the landform and natural vegetative characteristics of a site.

City of Kingston By-Law Number 2018-15, “Tree By-Law”
Page 8 of 23

(50) “Tree” means any species of woody perennial plant, including its root system, which has reached or can reach a height of at least 4.5 metres at physiological maturity.

(51) “Tree Permit” means the formal written approval from the Director to Destroy or Injure Trees, with or without conditions.

(52) “Tree Preservation and Protection Plan” means a plan prepared by a Certified Arborist and approved by the Director, that includes measures required to eliminate or mitigate the potential risk of Tree damage.

(53) “Tree Protection Zone” means an area surrounding a Tree that is marked and fenced off, where storage of materials of any kind, parking or moving of vehicles, and disturbance of the soil or grade is prohibited.

(54) “Urban Area” means the area within the Urban Boundary as defined in the Official Plan as indicated on Schedule ‘B’ of this By-Law.

(55) “Urban Boundary” means lands on full municipal services as defined in the Official Plan and indicated on Schedule ‘B’ of this By-Law.

(56) “Woodlands” means treed areas that provide environmental and economic benefits to both the private landowner and the general public, such as erosion prevention, hydrological and nutrient cycling, provision of clean air and the long-term storage of carbon, provision of wildlife habitat, outdoor recreational opportunities, and the sustainable harvest of a wide range of woodland products, and that have a quantity of Trees of a specific size as defined in the Forestry Act, RSO 1990, c F.26, that is more than one (1) hectare in area.

(By-Law Number 2018-15; 2021-111)

Application of the By-Law
This By-Law pertains to all lands within the geographic limits of the City of Kingston which include the Urban Area and Rural Area as shown on Schedule B and shall apply to:
(a) The Injury or Destruction of Trees that are 15 centimetres or greater in Diameter at Breast Height;

(b) The Injury or Destruction of Tree species classified as “extirpated”, “endangered”, “threatened”, or of “special concern”, as outlined in the provincial Endangered Species Act, 2007, SO 2007, c. 6;

© The Injury or Destruction of Tree species defined as “extirpated”, “endangered”, or “threatened”, or identified to be of “special concern” in the federal Species at Risk Act, SC 2002, c. 29;

(d) The Injury or Destruction of Trees classified as a Distinctive Tree as shown on Schedule A;

City of Kingston By-Law Number 2018-15, “Tree By-Law”
Page 9 of 23

(e) The Injury or Destruction of Trees located in areas designated Environmental Protection Areas (EPA) or as Open Space, as identified within the Official Plan;

(f) The Injury or Destruction of Trees that are within Significant Woodlands as identified within the Official Plan and indicated on Schedule ‘C’ of this By-Law;

(g) The Injury or Destruction of Trees that have been identified for protection in a Tree Preservation and Protection Plan approved by the Director;

(h) The Injury or Destruction of Trees on property owned by the City;

(i) The Injury or Destruction of Trees necessary to construct a “renewable energy project” as defined and regulated under the Green Energy Act, 2009, SO 2009, c. 12, Schedule A and

(j) The Injury or Destruction of Trees for the purposes of Clear Cutting.

General Prohibitions
3. No Person shall Injure or Destroy a Tree or cause the Injury or Destruction of a Tree:
(a) Unless exempted by Section 5, 6 or 7 of this By-Law; or

(b) Unless in possession of a Tree Permit issued under this By-Law and in accordance with its terms and conditions.

4. No Person shall:
(a) Contravene the terms or conditions of a Tree Permit issued under this By-Law; or

(b) Fail to comply with an order issued under this By-Law.

Exemptions - Urban Area and Rural Area
Despite Section 2 of this By-Law, this By-Law does not apply to the following activities in the Urban Area and Rural Area of the municipality:
(a) The Injury or Destruction of a Tree(s) undertaken by a municipality or a local board of a municipality;

(b) The Injury or Destruction of a Tree(s) undertaken under a license issued under the Crown Forest Sustainability Act, 1994, SO 1994, c. 25;

© The Injury or Destruction of a Tree(s) by a person licensed under the Surveyors Act, RSO 1990, c. S.29 to engage in the practice of cadastral surveying or his or her agent, while making a survey;

City of Kingston By-Law Number 2018-15, “Tree By-Law”
Page 10 of 23

(d) The Injury or Destruction of a Tree(s) imposed after December 31, 2002 as a condition to the approval of a site plan, a plan of subdivision, consent or part lot control under Sections 41, 51 or 53, respectively, of the Planning Act or as a requirement of a site plan agreement or subdivision agreement entered into under those sections;

(e) The Injury or Destruction of a Tree(s) by a transmitter or distributor, as those terms are defined in Section 2 of the Electricity Act, 1998, SO 1998, c. 15, Schedule A for the purpose of constructing and maintaining a transmission system or a distribution system, as those terms are defined in that section;

(f) The Injury or Destruction of a Tree(s) undertaken on land described in a license for a pit or quarry or a permit for a wayside pit or wayside quarry issued under the Aggregate Resources Act; RSO 1990, c. A.8;

(g) The Injury or Destruction of a Tree(s) undertaken on land in order to lawfully establish and operate or enlarge any pit or quarry on land,

(i) that has not been designated under the Aggregate Resources Act or a predecessor of that Act, and

(ii) on which a pit or quarry is a permitted land use under a by-law passed under Section 34 of the Planning Act;

(h) The Injury or Destruction of a Tree(s) undertaken on land within a Closure Plan which has been acknowledged to have been completed in accordance with the Mining Act by the Ministry of Northern Development and Mines.

The Injury of Destruction of a Tree(s) undertaken on land in order to lawfully establish and operate or enlarge any mine on land,

(i) that is not identified within a Closure Plan which has been acknowledged to have been completed in accordance with the Mining Act by the Ministry of Northern Development and Mines, and

(ii) on which a mine is a permitted land use under a by-law passed under Section 34 of the Planning Act.

(i) Pruning necessary to maintain the health and condition of the Tree, provided the pruning is in accordance with Good Arboricultural Practices;

(j) The Injury or Destruction of a Dead, Diseased, or severely Injured Tree(s), or a portion of such a Tree(s). A letter of opinion confirming the condition of the tree and the need for the removal may be required by a Qualified Person to the satisfaction of the City. Any such Injury or Destruction of a Tree(s) must be conducted in accordance with Good Arboricultural Practices;

(k) The Injury or Destruction of an Ash Tree(s) (Fraxinus spp.);

Page 11 of 23
(l) The Injury or Destruction of a Tree(s) as part of Emergency Work;

(m) The Injury or Destruction of a Tree(s) that are causing, or are likely to cause, structural damage to load-bearing walls or other structures as determined by a Qualified Person;

(n) The Injury or Destruction of a Tree(s) located within a building or structure,a solarium, a rooftop garden, or an interior courtyard;

(o) The Injury or Destruction of a Tree(s) required to permit the establishment or extension of a building or structure, including driveways and access routes, provided:

(i) the proposed use is permitted by the Zoning By-Law;

(ii) there is no reasonable alternative to the Injury or Destruction;

(iii) a Building Permit has been issued for the proposed building or structure or extension; and

(iv) no Tree is Destroyed or Injured that is located more than 15 metres from the outer edges of the existing building or structure and the outer edges of the expanded building or structure;

§ The Injury or Destruction of a Tree(s) necessary to install, provide or maintain utilities or public or private water and sanitary sewer infrastructure required for the construction or use of a building or structure for which a Building Permit has been issued;

(q) The Injury or Destruction of a Tree(s) that are protected under the Endangered Species Act for which the landowner has obtained approval from the Ontario Ministry of Natural Resources and Forestry to remove the Tree(s);

® The Injury or Destruction of a Tree(s) located within a cultivated orchard, Tree farm, or Plant Nursery that is being actively managed and harvested for the purposes for which the Trees were planted;

(s) The Injury or Destruction of a Tree(s) required as part of the operation of an existing cemetery or golf course; and

(t) The Injury or Destruction of a Tree(s) necessary to clear land in accordance with Normal Farm Practice conducted by an Agricultural Operation for its own agricultural purposes.

The Injury or Destruction of a Tree(s) located within a Significant Woodland or an Environmental Protection Area may be permitted provided that the activity is associated with a Normal Farm Practice. Whether a farm practice is a Normal Farm Practice shall be determined in accordance with the provisions of the Farming and Food Production Protection Act, including final arbitration by the Farm Practices Protection Board, as required.

Page 12 of 23

Exemption – Urban Area only
Despite Section 2 of this By-Law, this By-Law does not apply to the following:
(a) The Injury or Destruction of a Tree(s) located within the limits of any lot that permits a residential use and is occupied by a Residential Unit that was constructed prior to the passage of this By-Law.

(b) The Injury or Destruction of a Tree(s) located within the limits of any lot that permits a residential use and was created by way of a registered plan of subdivision, consent, part lot control, or a registered plan of condominium.

© Notwithstanding Section 6.(a) and 6.(b) of this By-Law to the contrary, the Injury or Destruction of a Tree(s) within an Environmental Protection Area and/or a Significant Woodland is not exempt from this By-Law and will not be permitted unless it has been demonstrated through the completion of an Environmental Impact Assessment (EIA), to the satisfaction of the City, that the Injury or Destruction can be supported.

Exemptions - Rural Area only
Despite Section 2 of this By-Law, this By-Law does not apply to the following activities in the Rural Area:
(a) The Injury or Destruction of Trees that are otherwise exempt from this By-law as indicated in Section 5, 6 and 7, which include Dead, Diseased or Hazard Trees for the purpose of Personal Use or Commercial Harvesting.

(b) The Injury or Destruction of Trees for the Owner’s Personal Use, provided that:

i. for properties less than 5 hectares in area, no more than ten (10) Cords of wood are to be removed within a consecutive period of twelve (12) months.

ii. for properties greater than 5 hectares and less than 10 hectares in area,no more than twenty (20) Cords of wood are to be removed within a consecutive period of twelve (12) months.

iii. for properties greater than 10 hectares in area, no more than thirty (30) Cords of wood are to be removed within a consecutive period of twelve (12) months.

© The Injury or Destruction of a Tree(s) on land for which a Forest Management Plan, approved by a Registered Professional Forester has been prepared, a copy of which has been submitted to the Director, and provided any Injury or Destruction is undertaken in accordance the Forest Management Plan;

Page 13 of 23

(d) The Injury or Destruction of a Tree(s) for Commercial Harvesting, where permitted by the applicable zoning by-law, provided that no more than ten (10) Cords of wood per one (1) hectare of Woodland are removed within a consecutive period of twelve (12) months;

(e) The Destruction or Injury of a Tree(s) for Personal Use, Commercial Harvesting or those subject to a Forest Management Plan must be completed in accordance with Good Arboricultural Practices and Good Forestry Practices and shall not result in Clear Cutting;

(f) The Injury or Destruction of a Tree(s) undertaken through Selective Harvesting for Personal Use, Commercial Harvesting, or those subject to a Forest Management Plan, proposed in an Environmental Protection Area and/or Significant Woodland may occur in the Rural Area as an exemption to this By-Law.

Where the Injury or Destruction of a Tree(s) within an Environmental Protection Area and/or Significant Woodland are not to be undertaken through Selective Harvesting, the Injury or Destruction of a Tree(s) must be justified through the completion of an Environmental Impact Assessment (EIA), to the satisfaction of the City and a permit will be required.

Tree Permits
Permit Application Process
Every Person that intends to Injure or Destroy a Tree, either personally or through another Person, shall:
(a) Submit a complete application for a Tree Permit in the form prescribed by the City;

(b) Pay the required fee as set out in the City’s Fees and Charges By-Law in place at the time of the application;

© Where prescribed by this By-Law or required by the Director, submit an Environmental Impact Assessment (EIA). The EIA shall be prepared by a Qualified Person and shall include the following:

(i) A description of the proposal and rationale for undertaking the Tree removal activity where proposed;

(ii) A survey illustrating the legal boundaries of the property, any easements, rights-of-way or other encumbrances;

(iii) An inventory and description of the key features present and their significance, including a reference to all Natural Heritage Features and Areas and their associated Ecological Functions;

City of Kingston By-Law Number 2018-15, “Tree By-Law”
Page 14 of 23

(iv) A professional opinion by the Qualified Person as to whether the proposal is acceptable considering potential impacts to Natural Heritage Features and Areas and their Ecological Functions taking into account the relevant policies of the Provincial Policy Statement and the Official Plan; and

(v) A description of any mitigation required to protect the Ecological Function of identified Natural Heritage Features and Areas.

(d) Where required by the Director, submit a report prepared by a Certified Arborist setting out the reasons for the proposed Injury and/or Destruction of the Tree(s) and the Tree Preservation and Protection Plan for any Trees to be retained. The report shall be prepared in accordance with the City of Kingston’s Guidelines for the Completion of an Arborist Report and the Guidelines for Tree Preservation and Protection.

(e) A Tree Permit Application shall only be considered complete when accompanied by the information required pursuant to this Section.

When all the requirements set out in Section 8 have been met, the Director will review the complete Tree Permit Application and may:
(a) Issue a Tree Permit;

(b) Issue a Tree Permit with conditions; or

© Refuse to issue a Tree Permit.

10. The Director may refuse to issue a Tree Permit where:
(a) The Injury or Destruction of a Tree(s) can be avoided, or ought to be avoided, as confirmed by a Qualified Person;

(b) The Injury or Destruction of a Tree(s) within an Environmental Protection Area, Open Space and/or Significant Woodland would have a Negative Impact on identified Natural Features and Areas and/or their Ecological Functions.

© An application for development approvals which relies on the Injury or Destruction of a Tree(s) has been made pursuant to the requirements of the Planning Act but for which a decision has not yet been rendered;

(d) The Injury of Destruction of a Tree(s) will negatively impact erosion or flood controls; and

(e) The Injury or Destruction of a Tree(s) will undermine the objectives of this By-Law as determined by the Director.

Page 15 of 23

Term of a Tree Permit
(1) A Tree Permit issued by the Director shall remain in effect for twelve (12)months after the date of issuance.
(2) A Tree Permit may be renewed for a period of up to two (2) additional years, upon the receipt of a written request from the Applicant at least thirty (30) days prior to its expiry, provided that the Director is satisfied, in his or her sole discretion, that there are reasonable grounds for the renewal.

(3) No Tree Permit shall be renewed where the Owner or Applicant is in breach of any of the provisions of this By-Law or the terms and conditions of the Tree Permit.

(4) Every application to renew a Tree Permit shall be accompanied by the applicable fee as set out in in the City’s Fees and Charges By-Law in place at the time of application.

Permit Conditions
(1) The Director may impose any conditions on a Tree Permit that are reasonable, which may include, but are not restricted to:
(a) Measures that will ensure the Injury or Destruction of a Tree(s) is carried out in accordance with Good Arboricultural Practice and Good Forestry Practice, which may include limitations on the manner and timing of the Injury or Destruction;

(b) Conditions recommended by a Qualified Person through the completion of an Environmental Impact Assessment (EIA) or other technical evaluation;

© Mitigative measures to protect against the Injury or Destruction of a Tree(s) that is not subject to removal, which may include the identification of Tree Zones;

(d) A requirement to prepare additional technical documentation that will be used to validate the appropriateness of issuing a Tree Permit and may include: an Environmental Impact Assessment; Landscaping, Replanting and Replacement Plan; a Sivicultural Prescription; a Forest Management Plan; and/or a Tree Preservation and Protection Plan;

(e) A requirement to provide compensation in accordance with Section 17 of this By-Law;

City of Kingston By-Law Number 2018-15, “Tree By-Law”
Page 16 of 23
(f) A requirement to enter into an agreement with the City which sets out the Owner’s obligations to replace Trees and any conditions imposed in accordance with this By-Law; and,

(g) A requirement to provide financial security for the performance of the Owner’s obligations under the agreement.

(1) All Trees that are to be Injured and/or Destroyed in accordance with an approved Tree Permit shall be marked by a Certified Tree Marker or Certified Arborist with clearly visible marks of orange paint both at 1.37 metres above ground level and at ground level, at least five (5) days prior to Destroying any Tree, but not prior to the issuance of a Tree Permit.
(2) The Applicant shall ensure that each stump remaining after cutting shall show the paint marking applied by the Certified Tree Marker or Certified Arborist.

(1) The Applicant shall cause the installation of all required Tree preservation measures under the supervision of a Certified Arborist to the satisfaction of the Director.
(2) The Applicant shall ensure that Tree preservation measures and Tree Protection Zone(s) are inspected by a Certified Arborist and a bi-monthly report is provided to the Director for the duration of the active period of Tree Injury and/or Destruction. Once Tree removals have been completed,a final report is required to confirm that the Tree(s) that were to remain on the site were not damaged during construction.

(1) A copy of the Tree Permit shall be posted on the property prior to the commencement of any Injury or Destruction of any Tree authorized by the Tree Permit in a conspicuous place on the property that is adjacent to a public road and visible to all persons, or at such other location designated by the Director.

(1) A Tree Permit may be revoked by the Director under any of the following circumstances:

(a) If it was issued based on mistaken, misleading, false, or incorrect information;

(b) If the Owner or Applicant requests, in writing, that it be revoked;

© If the terms of an agreement entered into pursuant to this By-Law are not complied with; or

(d) If an Owner fails to comply with any provision of the Tree Permit or this By-Law.

Page 17 of 23

(2) Once the Applicant has received written notice that the Tree Permit has been revoked, the Owner and/or Applicant shall immediately cease all operations being conducted under the authority of the revoked Tree Permit.

Compensation
(1) An Applicant for a Tree Permit will be required to pay financial compensation when replacement Trees cannot be accommodated on the property.
(2) Financial compensation must be provided in the form of cash or an irrevocable letter of credit in Canadian currency and must be provided to the City in advance of the issuance of a Tree Permit.

(3) When replacement Trees can be accommodated on the property, the quantity, species and size of replacement Trees shall be equivalent in value to the value of the Tree(s) Injured or Destroyed as a result of the issuance of the Tree Permit. The City will require financial securities when replacement Tree(s) are proposed in association with a Tree Permit.

(4) The value of financial compensation or financial securities shall be calculated as follows:

(a) The value of any Tree that is Injured or Destroyed as part of an approved plan of subdivision may be determined using a per-Tree flat rate compensation value as indicated in the City’s Subdivision Development Guidelines and Technical Standards, as amended and applied as follows:

(i) Trees in poor condition will be exempted and will not be used to calculate compensation amounts;

(ii) Ash Trees (Fraxinus spp.) will be exempted and will not be used to calculate compensation amounts;

(iii) Trees in moderate condition, regardless of size, will be given a compensation value based on a one replacement Tree to one Tree removed ratio (1:1);

(iv) Trees in good condition, regardless of size, will be given a compensation value based on a two replacement Tree to one Tree removed ratio (2:1); and

City of Kingston By-Law Number 2018-15, “Tree By-Law”
Page 18 of 23

(v) Trees located within a proposed road allowance or area required to accommodate public infrastructure (e.g., stormwater management facility, utility corridors, public servicing infrastructure - water, sewer and storm, etc.) as identified in an existing Secondary Plan or an approved Draft Plan of Subdivision may be exempted from the calculation of compensation amounts where it can be demonstrated that efforts have been made to avoid wooded areas in the design of the plan; or

(b) The value of any Tree that is Injured or Destroyed and is not part of an approved plan of subdivision will be determined using the International Society of Arboriculture Trunk Formula Method, as amended from time to time, or

© The Director may determine an alternate method for the calculation of any financial compensation or financial security in consultation with City Forestry staff where it can be demonstrated that the objectives of this By-Law and the broader objectives of the City will be achieved.

Agreements, Security and Replacement Trees
(1) Owners will be required to enter into an agreement with the City when financial securities are required as a condition of a Tree Permit.
(2) Financial securities must be provided in the form of cash or an irrevocable letter of credit in Canadian currency and must be provided to the City in advance of the issuance of a Tree Permit.

(3) When associated with Tree replacement, financial securities shall be deposited with the City and will be held for a minimum of two (2) years after planting. The securities will be released upon the City’s confirmation of the survival of the replacement Tree(s) beyond the two (2) year period. If replacement Tree(s) do not survive the two (2) year period, the City may draw upon the financial securities to execute the replacement of any unhealthy or deceased Tree(s).

(4) Where an Owner has made an application for development approvals in accordance with the Planning Act and has been issued a Tree Permit which required the posting of financial securities, the amount of any financial security to be collected by the City as part of the Planning Act application may be reduced provided the value of the works, specifically associated with landscaping, meets or exceeds the value of the securities tied to the Tree Permit.

Page 19 of 23

Appeals to City Council
(1) An Applicant for a Tree Permit may appeal in writing to Council of the City if the City refuses to issue a Tree Permit, within thirty (30) days after the refusal.
(2) An Applicant for a Tree Permit may appeal in writing to the Council of the City if the Applicant objects to a term or condition of the Tree Permit, within thirty (30) days after the issuance of the Tree Permit.

(3) An Applicant shall submit an appeal in writing, by way of registered mail,to the City Clerk.

(4) The Director shall prepare and forward a report to Council that sets out the reasons for the refusal of the Tree Permit or reasons for the terms and conditions of the Tree Permit, as the case may be.

(5) On appeal, Council has the same powers as the Director and may make a decision to:

(a) Issue a Tree Permit, with or without conditions;

(b) Confirm the refusal to issue the Tree Permit; or

© Affirm, vary, or add any conditions to the Tree Permit.

(6) The decision made by Council on the appeal of the Tree Permit is final.The Clerk will notify the Applicant in writing of Council’s decision within five (5) business days.

Enforcement
(1) Council hereby delegates to the Director the authority to enforce this By-Law, to issue Tree Permits under this By-Law and to impose terms and conditions to such permits.
(2) The Director may appoint from time to time, persons to act as Officers to administer and enforce the provisions of this By-Law.

(3) An Officer may enter on land at any reasonable time for the purpose of carrying out an inspection to determine whether or not this By-Law, an Order, or a condition of a Tree Permit is being complied with.

(4) An Officer, in carrying out an inspection pursuant to Section 20(3) may be accompanied by the Director, and any other Person necessary to assist the Officer with his or her enforcement activities.

(5) An Officer carrying out an inspection pursuant to Section 20(3) may:

(a) require the production for inspection of documents or things relevant to the inspection;

City of Kingston By-Law Number 2018-15, “Tree By-Law”
Page 20 of 23

(b) inspect and remove documents or things relevant to the inspection for the purpose of making copies or extracts;

© require information from any person concerning a matter related to the inspection; and

(d) alone or in conjunction with a person possessing special or expert knowledge, make examinations or take tests, samples or photographs necessary for the purposes of the inspection.

(6) No person shall hinder or obstruct, or attempt to hinder or obstruct, any person who is exercising a power or performing a duty under this By-Law.

(7) Where an Officer has reasonable grounds to believe that an offence under this By-Law has been committed by a Person, the Officer may require the name, address, and proof of identity of that Person.

(8) Failure to provide proof of identification satisfactory to a Provincial Offences Officer when requested to do so pursuant to Section 20 (7) of this By-Law shall constitute obstruction of an Officer under Section 20 (6)of this By-Law.

(By-Law Number 2018-15; 2021-111)

Orders
(1) Where the Director is satisfied that a contravention of this By-Law has occurred, the Director may issue an Order to Discontinue requiring the person who contravened the By-Law, or who caused or permitted the contravention, or the Owner or occupier of the land on which the contravention of the By-Law occurred, to discontinue the contravening activity.
(2) The Order to Discontinue shall set out reasonable particulars of the contravention adequate to identify the contravention, the location of the land on which the contravention occurred and the date by which there must be compliance with the Order.

(1) Where the Director is satisfied that a contravention of this By-Law has occurred, the Director may issue an Order requiring the Person who contravened the By-Law or who caused or permitted the contravention, or the Owner or occupier of the land on which the contravention occurred, to do the work specified in the Order that is necessary in the opinion of the Director to correct the contravention, including without limitation the planting of replacement Tree(s) in accordance with Section 18 of this By-Law.
City of Kingston By-Law Number 2018-15, “Tree By-Law”
Page 21 of 23

(2) The Order shall set out the reasonable particulars of the contravention adequate to identify the contravention, the location of the land on which the contravention occurred, if applicable, and the date by which there must be compliance with the Order.

(3) The Order may provide that if the person named in the Order fails to comply with the Order by a date specified in the Order, that the City shall have the right to enter upon the land affected by the Order at any time, and to complete the work specified in the Order at the expense of the person named in the Order and may draw on any financial security provided by the Owner to complete the work.

23.(1)An Order to Discontinue issued under Section 21, or an Order issued under Section 22, may be:

(a) served personally by an Officer on the Owner, Applicant or any other Person who caused or permitted the contravention;

(b) posted in a conspicuous place on the property where the contravention occurred; or

© sent by registered mail to the Owner, Applicant or any other Person who caused or permitted the contravention of this By-Law.

(2) Where an Order issued under this By-Law is served personally by an Officer, it shall be deemed to have been served on the date of delivery to the Person(s) named.

(3) The posting of the Order on the property where the contravention took place shall be deemed to be sufficient service of the Order on the Person named in the Order on the date it is posted.

(4) Where an Order issued under this By-Law is sent by registered mail, it shall be sent to the last known address of the Person named in the Order and shall be deemed to have been served on the fifth (5th) day after the Order is mailed.

24.(1)If a Person fails to comply with an Order issued pursuant to Section 21 of this By-Law, the City may enter the lands at any reasonable time for the purposes of doing the things described in the Order at the Person’s expense.

(2) If the City enters on the lands and completes the work, the City may recover its costs to complete the work from the Person named in the Order by drawing upon the financial security, or by action, or by adding the costs to the tax roll and collecting them in the same manner as property taxes. Costs owning to the City will accrue at a rate of fifteen (15) percent annually and may also be registered as a lien against the property subject to the Tree Permit.

City of Kingston By-Law Number 2018-15, “Tree By-Law”
Page 22 of 23

Penalties
(1a)
Every Person who contravenes any provision of this By-Law shall, upon issuance of a Penalty Notice in accordance with Administrative Penalty Process By-Law 2020-69, be liable to pay to the City an Administrative Penalty as set out in Schedule B of the Administrative Penalty Process By-Law.

(By-Law Number 2018-15; 2021-111)

25.(1)Nothwithstanding Part 25 (1a) of this By-Law, every Person who

contravenes a provision of this By-Law is guilty of an offence.

(By-Law Number 2018-15; 2021-111)

(2) Every Person who contravenes an Order under Section 21 or Section 22 of this By-Law is guilty of an offence.

26.(1)A Person who is convicted of an offence under this By-Law is liable, for each day or part of a day that the offence continues, to a maximum of Ten Thousand ($10,000) Dollars, and the total of all daily fines is not limited to One Hundred Thousand ($100,000) Dollars.

(2) If a Person is required to pay an Administrative Penalty under section 25(1a) in respect of a contravention of this By-Law, the Person shall not be charged with an offence in respect of the same contravention.

(3) In accordance with section 351 of the Municipal Act, 2001, as amended from time to time, the treasurer of the City may add unpaid fees, charges and/or fines issued under this By-Law to the tax roll and collect them in the same manner as property taxes.

(4) When a Person is convicted of an offence under this By-Law, the conditions of a Tree Permit, or an Order issued under this By-Law, the Court in which the conviction has been entered, and any Court of competent jurisdiction thereafter, may, in addition to any fine imposed,make an order:

(a) Prohibiting the continuation or repetition of the offence; and

(b) Requiring the Person convicted to correct the contravention in the manner and within the period that the court considers appropriate, including requiring the person to abide by any term or condition of the Tree Permit, rehabilitate the land, plant or replant Trees, or perform any Silviculture treatment necessary to re-establish the Trees, or provide compensation.

(By-Law Number 2018-15; 2021-111)

Administration
27.(1)The short title of this By-Law is the “Tree By-Law”.
(2)Schedule ‘A’ and Schedule ‘B’ shall form part of this By-Law.

(3)References to any statute or any provision thereof include such statute or provision as amended, revised, re-enacted and/or consolidated from time to time, and any successor statute.

(4) If any Section or Sections of this By-Law or parts thereof are found by any Court of competent jurisdiction to be illegal or beyond the power of the Council to enact, such Section or Sections or parts thereof shall be deemed to be severable and all other Sections or parts of this By-Law shall be deemed to be separate and independent therefrom and continue in full force and effect.

(5) If there is a conflict among this By-Law and a By-Law passed under the Forestry Act, Municipal Act, or the Heritage Act, the provision that is the most restrictive regarding the Injury or Destruction of Trees shall prevail.

(6) Nothing in this By-Law shall exempt any Person from complying with the requirements of any other by-law in force, or from obtaining any license, permission, permit, authority or approval required under any other by-law or legislation.

(7) Any application received prior to the passage of this By-Law, will be processed in accordance with the provisions of By-Law 2007-170, as amended.

(8) A five year review of this By-law shall be undertaken to assess and monitor the effectiveness of its provisions.

This By-Law was given all Three Readings and Passed: December 19, 2017

Note: schedule pages attached to the PDF formatted By-law only.

Schedule ‘A’ - List of Distinctive Tree Species
The following is a list of Distinctive Tree species that are considered to be uncommon to the City of Kingston region and environment:

Common English Name	Latin Name
Black Maple	Acer nigrum
Ginkgo	Ginkgo biloba
Kentucky CoffeeTree	Gymnocladus dioica
Black Walnut	Juglans nigra
Sycamore	Platanus occidentalis
London PlaneTree	Platanus x acerifolia
Tulip-Tree	Liriodendron tulipifera
Ohio Buckeye	Aesculus glabra
Pitch Pine	Pinus rigida
Douglas-Fir	Pseudotsuga menziesii
Schedule ‘B’ to By-Law Number 2018-15 “Tree By-Law”
"""
NUISANCE_PARTIES_TEXT = """

Nuisance Parties Bylaw
Bylaw #: 2018-53

Description: Regulate nuisance parties within the City of Kingston

Date passed: March 20, 2018

Disclaimer: Bylaws contained in this section have been prepared for research and reference purposes only. The original Nuisance Party Bylaw in pdf format is available from the Ofice of the City Clerk upon request.

Introduction
Whereas section 425 of the Municipal Act, 2001 provides that a municipality may pass By Laws providing that a person who contravenes a Bylaw of the municipality passed under that Act is guilty of an ofence; and

Whereas section 429 of the Municipal Act, 2001 provides that a municipality may establish a system of fnes for ofences under a Bylaw of the municipality passed under that Act; and

Whereas section 10 of the Municipal Act, 2001 provides that a municipality may pass Bylaws respecting: economic, social and environmental well-being of the municipality; heath, safety and well-being of person; the protection of persons and property; and structures, including fences and signs; and

Whereas section 128 of the Municipal Act, 2001 provides that a local municipality may prohibit and regulate with respect to public nuisances, including matters that, in the opinion of Council, are or could become or cause public nuisances, and the opinion of Council under this section, if arrived at in good faith, is not subject to review by any court; and

Whereas section 391 of the Municipal Act, 2001 provides that a municipality may impose fees or charges on persons for services provided or done by or on behalf of it, including costs incurred by the municipality related to enforcement, whether or not it is mandatory for the municipality to provide or do the service; and

Whereas sections 435 and 436 of the Municipal Act, 2001 provide for the exercise of powers of entry of a municipality; and

Whereas section 444 of the Municipal Act, 2001 provides that a municipality may make an Order requiring a person who contravened a Bylaw or who caused or permitted contravention, or the owner or occupier of the land on which the contravention occurred to discontinue the contravening activity; and

Whereas section 434.1(1) of the Municipal Act, 2001 provides that a municipality may require a person, subject to such conditions as the municipality considers appropriate, to pay an administrative penalty if the municipality is satisfed that the person has failed to comply with a bylaw of the municipality passed under this Act; and

Whereas section 431 of the Municipal Act, 2001 provides that if any Bylaw of a municipality passed under that Act is contravened and a conviction entered, in additional to any other remedy and to

any penalty imposed by the Bylaw, the court in which the conviction has been entered and any court of competent jurisdiction thereafter may make an order prohibiting the continuation or repetition of the ofence by the person convicted; and

Whereas in the opinion of Council, the matters addressed in this Bylaw are, or could become or cause public nuisances, and, notwithstanding the generality of the foregoing, Council is of the opinion that a Nuisance Party (as defned herein) is a public nuisance;

Therefore be it resolved that the Council of The Corporation of the City of Kingston enacts as follows:

Part 1 - Defnitions

For the purposes of this Bylaw:

Administrative Penalty means an administrative penalty administered pursuant to "Bylaw 2020-69 of the Corporation of the City of Kingston being “A Bylaw to Establish a Process for Administrative Penalties”;

Chief of Police means the Chief of Police of the Kingston Police, or their designate;

City means The Corporation of the City of Kingston;

Highway includes a common and public highway, avenue, parkway, driveway, square, place, bridge, viaduct or trestle, any part of which is intended for or used by the general public for the passage of vehicles or persons, and includes the area between the lateral property lines thereof, including sidewalks and boulevards;

Municipality means the land within the geographic limit of the City of Kingston;

Nuisance Party means a gathering on Premises which, by reason of the conduct of any one or more of the Person(s) in attendance, is characterized by any one or more of the following elements:

a. public intoxication;

b. the unlawful sale, furnishing, or distribution of alcoholic beverages or controlled substances;

c. the unauthorized deposit of refuse on public or private property;

d. damage to public or private property;

e. the obstruction of vehicular or pedestrian trafic, or interference with the ability to provide emergency services;

f. sound that is unusual or excessive, or that is likely to be unwanted by or disturbing to persons, including but not limited to loud music or shouting;

g. unauthorized open burning or the display of unauthorized freworks;

h. public fghts;

i. outdoor public urination or defecation;

j. use of or entry upon a roof not intended for such occupancy;
Oficer means a Provincial Ofences Oficer of the City who has been assigned the responsibility of administering or enforcing this Bylaw, or an oficer of the Kingston Police or other police force assisting the Kingston Police;

Penalty Notice means a notice given pursuant to sections 2.2 and 2.4 of "Bylaw 2020-69 of the Corporation of the City of Kingston being “A Bylaw to Establish a Process for Administrative Penalties”;

Person means a corporation as well as an individual;

Premises means any public or private place in the Municipality, including but not limited to Highways, parks, parking lots, yards appurtenant to a building or dwelling, or vacant lands.

Part 2 - Administration
2.1 The City’s Licensing and Enforcement Division is responsible for the administration of this Bylaw.

Part 3 - Interpretation
3.1 This Bylaw shall not be interpreted as exempting any Person from the requirement to comply with any other City Bylaw. In the event of confict between the provisions of this Bylaw and any other City Bylaw, the provisions which are more protective of the public assets of the City, the economic, social and environmental well-being of the City, the health, safety and well-being of persons in the City, and persons and property in the City, shall apply.

3.2 Any reference herein to any Bylaw or Act of any government shall be construed as a reference thereto as amended or re-enacted from time to time or as a reference to any successor thereto then in force.

Part 4 - Regulation of Nuisance Parties
4.1 No Person shall create, cause, host, sponsor, conduct, continue, or permit a Nuisance Party.

4.2 Upon the Order of the Chief of Police, a Nuisance Party shall cease and all Persons not residing at the Premises where the Nuisance Party is occurring shall immediately leave the Premises.";

4.3 An Order under section 4.2 of this Bylaw shall identify:

a. the Premises at which the contravention occurred; and

b. the reasonable particulars of the contravention of this Bylaw.

4.4 An Order under section 4.2 of this Bylaw may be given verbally or may be served personally on the Person(s) to whom it is directed.

4.5 No Person shall fail to comply with an Order issued pursuant to section 4.2 of this Bylaw.

4.6 No Person who, individually or jointly with others, is an owner or who otherwise has rightful possession of or possessory control of any Premises, shall permit or allow a Nuisance Party to

occur on said Premises by failing to take reasonable steps within such Person’s control to mitigate the occurrence of a Nuisance Party on their Premises.

Part 5 - Close Public Highway
5.1 The Chief of Police, may temporarily close any Highway or portion thereof to public travel where a Nuisance Party is occurring on or adjacent to the Highway, in accordance with the Highway Trafic Act.

5.2 Where a Highway or portion of a Highway has been closed, the common law right of passage by the public over the Highway and the common law right of access to the Highway by an owner of land abutting the Highway are restricted, as directed by the Chief of Police.

5.3 No Person shall, without lawful authority, use a Highway or portion thereof that has been closed temporarily in accordance with section 5.1 of this Bylaw.

5.4 No Person shall, without lawful authority, remove or deface any barricade, fashing light, warning device, detour sign, notice or other device placed on a Highway that has been temporarily closed in accordance with section 5.1 of this Bylaw.

Part 6 - Additional Fees and Charges
6.1 Any Person who creates, causes, hosts, sponsors, conducts, continues or permits a Nuisance Party in contravention of this Bylaw, and any Person who permits or allows a Nuisance Party to occur on their Premises in contravention of section 4.6 of this Bylaw, shall be required to pay the fees and charges specifed in Bylaw Number 2005-10, A Bylaw to Establish Fees and Charges to be Collected by The Corporation of the City of Kingston, as amended from time to time, for the attendance of an Oficer, and/or an oficer of Kingston Fire & Rescue, at the scene of a Nuisance Party.

6.2 Fees and charges imposed on a Person pursuant to section 6.1 constitute a debt of the Person to the City.

6.3 Where the owner of the Premises at which the Nuisance Party occurs is responsible for paying the fees and charges set out in section 6.1, the City may add such fees and charges to the tax roll for the Premises and collect them in the same manner as property taxes.

Part 7 - Enforcement and Inspection
7.1 The provisions of this Bylaw may be enforced by an Oficer.

7.2 No Person shall obstruct or hinder or attempt to obstruct or hinder an Oficer or other authorized employee or agent of the City in the exercise of a power or the performance of a duty under this Bylaw.

7.3 Every Oficer shall have the right to enter lands and Premises to conduct an inspection to determine whether the provisions of this Bylaw and any order(s) issued hereunder are being complied with in accordance with the provisions of sections 435 and 436 of the Municipal Act,2001.

7.4 Where an Oficer has reasonable grounds to believe that an ofence under this Bylaw has been committed by a Person, the Oficer may require the name, address, and proof of identity of that Person.

7.5 Failure to provide proof of identifcation satisfactory to an Oficer when requested to do so pursuant to section 6.4 of this Bylaw shall constitute obstruction of an Oficer under section 6.2 of this Bylaw.

Part 8 - Penalty
8.1a Every Person who contravenes any provision of this Bylaw shall, upon issuance of a Penalty Notice in accordance with Administrative Penalty Process Bylaw 2020-69, be liable to pay to the City an Administrative Penalty in accordance with Schedule B of Administrative Penalty Process Bylaw 2020-69 for each day on which the contravention occurs, and the Administrative Penalty Process Bylaw 2020-69 applies to each Administrative Penalty issued pursuant to this Bylaw.

8.1 Notwithstanding section 8.1a of this Bylaw, every Person, other than a corporation, who contravenes any provision of this Bylaw is guilty of an ofence and on conviction is liable to a fne of not more than $10,000 for a frst ofence and $25,000 for any subsequent ofence.

8.2 Notwithstanding section 8.1a of this Bylaw, every corporation that contravenes any provision of this Bylaw and every oficer or director of a corporation who knowingly concurs in such contravention is guilty of an ofence and on conviction is liable to a fne of not more than $50,000 for a frst ofence and $100,000 for any subsequent ofence.

8.3 If this Bylaw is contravened and a conviction entered, the court in which the conviction has been entered and any court of competent jurisdiction thereafter may, in addition to any other remedy and to any penalty that is imposed, make an Order prohibiting the continuation or repetition of the ofence by the person convicted.

8.4 If a Person is required to pay an Administrative Penalty under section 8.1a in respect of a contravention of this Bylaw, the Person shall not be charged with an ofence in respect of the same contravention.

8.5 In accordance with section 351 of the Municipal Act, 2001, the treasurer of the City may add unpaid fees, charges and/or fnes issued under this Bylaw to the tax roll and collect them in the same manner as property taxes.

Part 9 - Validity
9.1 If a court of competent jurisdiction declares any provision, or any part of a provision, of this Bylaw to be invalid, or to be of no force and efect, it is the intention of Council in enacting this Bylaw that each and every provision of this Bylaw authorized by law be applied and enforced in accordance with its terms to the extent possible according to law.

Part 10 - Short Title of Bylaw
10.1 This Bylaw may be referred to as the “Nuisance Party Bylaw”.

Part 11 - Commencement
11.1 This Bylaw shall come into force and take effect on the date of its passing.
"""
PROPERTY_STANDARDS_TEXT = """

Property Standards Bylaw
Bylaw #: 2005-100

Description: Prescribes standards for the maintenance and occupancy of property within the City.

Date passed: May 17, 2005

Disclaimer: Bylaws contained in this section have been prepared for research and reference purposes only. The original Property Standards Bylaw in pdf format is available from the Ofice of the City Clerk upon request.

Introduction
Whereas there is in efect in the City of Kingston an Oficial Plan that provisions relating to Property Conditions;

And Whereas Section 15.1 (3) of the Building Code Act, 1992, S.O. 1992, c.23, as amended provides that a bylaw may be passed by the Council of a municipality prescribing the Standards for the maintenance and occupancy of property within the municipality provided the Oficial Plan for the municipality includes provisions relating to property conditions;

And Whereas the Council of The Corporation of the City of Kingston desires that a Bylaw be enacted pursuant to Section 15.1 (3) of the Building Code Act, 1992, S.O. 1992, c. 23 as amended within the limits of the City of Kingston,

And Whereas Sections 35.3 (1) and 45.1 (1) of the Ontario Heritage Act, 1990, c.0.18, as amended provide that a Bylaw may be passed by the Council a municipality prescribing minimum Standards for the Maintenance of the Attributes of Designated Heritage Properties within the municipality, and that Designated Heritage Properties that do not comply with those Standards Repaired and Maintained to conform with those Standards;

And Whereas Section 15.6 (1) of the Building Code Act, 1992, S.O. 1992, c. as amended requires that a Bylaw passed under Section 15.1 (3) of the Act provide for the establishment of a Property Standards Committee;

And Whereas the Council of The Corporation of the City of Kingston deems it desirable to enact and pass a Bylaw for prescribing Standards for the Maintenance and occupancy of Property within the City of Kingston and prohibiting the use of such property that does not conform to the Standards; and for requiring property below the Standards herein to be repaired and maintained to comply with the Standards, or the land thereof to be cleared of all buildings or structures and left in a graded and level condition;

And Whereas the Council of The Corporation of the City of Kingston deems it desirable to enact and pass a Bylaw for prescribing the minimum Standards for the Maintenance of the Heritage Attributes of Designated Heritage Properties within the municipality;

And Whereas subsection 15.4.1 (1) of the Building Code Act, 1992 provides that a municipality may require a person, subject to such conditions as the municipality considers appropriate, to pay an administrative penalty if the municipality is satisfed that the person has failed to comply with,

a. a bylaw of the municipality passed under section 15.1; or

b. an order of an oficer under subsection 15.2 (2) as deemed confrmed or modifed by the committee or a judge under section 15.3.

Part 1 - Defnitions
For the purposes of this Bylaw:

Accessory Building means a detached building, out-building or the use of which is incidental to the primary use of the Property;

Adequate means equal or amounting to what is suficient, ftting, suitable, equal to what is required;

Administrative Penalty means an administrative penalty imposed pursuant to City of Kingston Bylaw Number 2020–69, being "A Bylaw to Establish a Process for Administrative Penalties

Appeals Committee means the committee referred to in Section 15.6 of the Building Code Act, 1992, S.O. 1992, c. 23 as amended to hear appeals of Property standards orders issued under this Bylaw;

Basement means that space of a building that is partly below grade, has half or more of its height,measured from foor to ceiling, above average fnished grade;

Bathroom means a room containing a bathtub or shower with or without water closet and wash basin;

Built Heritage Specialist means a person with heritage experience and who is a member of the Canadian Association of Heritage Professionals and/or a member of the Royal Architectural Institute of Canada;

Cellar means that space of a building that is partly or entirely below which has more than half of its height, measured from foor to ceiling, the average fnished grade;

Character defning element (Deleted see Bylaw 2015-15)

City means The Corporation of the City of Kingston;

Crawl Space means an enclosed space between the underside of a assembly and the ground cover directly below, with a clearance less 1800 mm in height;

Designated Heritage Property means Property designated under Part or Part V under the Ontario Heritage Act, R.S.O. 1990, c.0.18, as amended;

Designation Bylaw means a Bylaw enacted by City Council pursuant to Section 29 or Section 41 of the Ontario Heritage Act, R.S.O. 1990, c.0.18, as amended that identifes Property and/or a defned area or areas to be of cultural heritage value or interest.

Director means the City’s Director of Licensing and Enforcement Services or their designate, or in the event of organizational changes, the director of the appropriately titled department;

Dwelling means a building or structure or part of a building or structure occupied or capable of being occupied in whole or in part or intended to be used for the purposes of human habitation;

Dwelling Unit means one room or two or more rooms connected as a separate unit in the same structure and constituting an independent for residential occupancy by humans for living and sleeping purposes;

Farm Buildings means any buildings or structures used in association with a farm use including any of the structures used in farming operations, which may include buildings to house livestock, machinery and crops, but does not include any residential building;

Grade means the average elevation of the fnished surface of the ground around the perimeter of a building excluding localized depressions such as, sunken terraces, stairwells and window wells.

Habitable Room means any room in a dwelling unit used or intended to be used for living, sleeping, cooking or eating purposes;

Heritage Attributes shall have the meaning set out in the Ontario Heritage Act, R.S.O. 1990, c.0.18, as amended and for greater certainty means:

a. in relation to real Property, and to the buildings and structures on the real Property, the attributes of the Property, buildings and structures that contribute to their cultural heritage value or interest and that are defned, described or that can be reasonably inferred:

i. in a Bylaw designating a Property passed under Section 29 of the Ontario Heritage Act, R.S.O. 1990, c.0.18, as amended and identifed as heritage attributes, values, reasons for designation or otherwise;

ii. in a Minister’s order made under Section 34.5 of the Ontario Heritage Act, R.S.O. 1990, c.0.18, as amended and identifed as heritage attributes, values, reasons for designation or otherwise;

iii. in a Bylaw designating a heritage conservation district passed under Section 41 of the Ontario Heritage Act, R.S.O. 1990, c.0.18, as amended and identifed as heritage attributes, values, reasons for designation or otherwise; or

iv. in the supporting documentation required for a Bylaw designating a heritage conservation district, including but not limited to a heritage conservation district plan, assessment or inventory, and identifed as heritage attributes, reasons for designation or otherwise;

b. the elements, features, or building components that support or protect the Heritage Attributes, without which the Heritage Attributes may not be conserved, including but not limited to roofs, walls, foors, retaining walls, foundations and structural systems;

Heritage Conservation District means a geographic district established under Part V of the Ontario Heritage Act, R.S.O.1990, c.O.18, as amended;

Heritage Conservation District Plan means a plan adopted by Council under Part V of the Ontario Heritage Act, R.S.O.1990, c.O.18, as amended to provide direction in the preservation of the Heritage Attributes of a Heritage Conservation District;

Hoarding means a fence or similar structure used to enclose a property or part thereof which is or intended to be under development, site alteration, or maintenance.

Inoperative Condition means not in working condition;

Listed Property means Property that City Council has determined to be cultural heritage value or interest;

Maintenance means the act of keeping up, preserving or conserving or paying to keep up, preserve or conserve property.

Medical Oficer of Health means the Medical Oficer of Health for the South East Health Unit;

Multiple Dwelling means a building containing three or more Units;

Multiple Use Building means a building containing both a Dwelling Unit and a Non-Residential Property;

Non-Habitable Room means any room in a Dwelling or Dwelling Unit other than a Habitable Room and includes Bathroom, boiler room, laundry, pantry, lobby, communicating corridor, stairway, closet, Basement, boiler room or other space for service and Maintenance of the Dwelling for public use, and for access to and vertical travel between storeys;

Non-Residential Property means a building or structure or part of a building or structure not occupied or capable of being occupied in whole or in part for the purposes of human habitation and includes the land and premises appurtenant thereto and all out-buildings, fences or erections thereon or therein;

Occupant means any person or persons over the age of 18 years who appears to be in possession of the property;

Oficer means a Property Standards Oficer and/or a Provincial Ofences

Oficer of the City who has been assigned the responsibility of administering and enforcing this Bylaw and includes the Chief Building Oficial or his or her designate;

Owner means any person having control over any portion of the building or Property and includes:

a. the person for the time being managing or receiving the rent of the land or premises in connection with which the word is used, whether on the person’s own account or as agent or trustee of any other person or who would receive the rent if such land and premises were let; and

b. a lessee or Occupant of the Property who, under the terms of a lease, is required to Repair and Maintain the Property in accordance with the Standards for the Maintenance and Occupancy of Property;

Penalty Notice means a notice given pursuant to sections 2.2 and 2.4 of City of Kingston Bylaw Number 2020–69, being “A Bylaw to Establish a Process for Administrative Penalties”;

Person means an individual, frm, corporation, association or partnership;

Property means a building or structure or part of a building or structure and includes the lands and premises appurtenant thereto and all mobile homes, mobile buildings, mobile structures, out-buildings, fences and erections thereon whether heretofore or hereafter erected and includes Vacant Property, Listed Property and Designated Heritage Property;

Reasonable means of such an amount, size and or number as is judged to be appropriate or suitable to circumstances or purpose; ft and appropriate to ends in view;

Repair includes the provision of such facilities or the taking of any as may be required so that the Property shall conform to the established in this Bylaw, including but not limited to restoring, and mending as a result of decay, dilapidation, or partial destruction (as fre);

Residential Property means any Property that is used or designed for use as a domestic establishment in which one or more persons usually sleep and prepare and serve meals, and includes any land or buildings that are appurtenant to such establishment and all steps, walks, driveways, parking spaces and fences associated with the Property or its Yard;

Sewerage System means the sanitary sewerage system under the control of the Corporation or of a private sewage disposal system company;

Sign means any surface upon which there is printed, projected or attached, any announcement, declaration or insignia used for direction, information, identifcation, advertisement, business promotion or promotion of products, activity or services, and includes a structure, whether in a fxed location or designed to be portable or capable of being relocated, or part thereof specifcally designed for the foregoing uses, including but not limited to fags, banners, advertising devices, blimps, balloons and models;

Standards means the standards of physical condition and of occupancy prescribed for Property by this Bylaw;

Toilet Room means a room containing a water
Waterfront Property means that area of water which is capable of use from the land together with that area of land adjacent to water which is necessary to allow use of the above area of water;

Yard means the land, other than publicly owned land, around or appurtenant to the whole or any part of a Residential or Non-Residential Property and used or intended to be used or capable of being used in connection with the Property and includes a Vacant Lot.

Part 2 - Applicability
2.1 This Bylaw shall apply to all Property within the limits of the City.

2.2 Notwithstanding Section 2.1, the following Properties are exempt from the requirements of this bylaw:

2.2.1 Property owned by the City and;

2.2.2 Farm Buildings and lands which are being used for agricultural and farm purposes and are located within an agricultural zone.

2.3 Notwithstanding Section 2.2, Farm Buildings located on Designated Heritage Properties are subject to the requirements of Part 7 of this Bylaw.

Part 3 - Administration
3.1 The Director is responsible for the administration and enforcement of this Bylaw.

3.2 The imperial measurements contained in this Bylaw are given for reference only.

Part 4 - General Standards for all Properties

4.1 General Standards set out in Section 4, the following regulations, shall apply to all Property within limits of the City.

4.2 All work, Repairs and Maintenance of Property shall be carried out with suitable and suficient materials and in a manner accepted as good workmanship and shall conform to all other Bylaws of the City, codes and statutes as applicable.

Accessory Buildings, Fences and Retaining Walls
4.3 Fences, barriers and retaining walls shall be kept in good repair.

4.4 Where fences or retaining walls have been painted or otherwise treated, they shall be maintained so as to be free of peeling paint or other coatings.

4.5 Accessory Buildings shall be kept in good repair.

4.6 Exteriors of Accessory Buildings shall be weather resistant. Where Accessory Buildings have been painted or otherwise treated, they shall be Maintained so as to be free of peeling paint or other coatings.

4.7 Where an Accessory Building, fence, retaining wall or the land may harbour an infestation of insects or rodents all necessary steps, in accordance with Bylaw Number 2008-28, ‘A Bylaw to Regulate the Use of Pesticides on Lawns Within the City of Kingston’, shall be taken to eliminate the insects or rodents and to prevent their reappearance.

Appliances
4.8 All appliances, equipment, accessories and installations provided by the Owner shall be installed and Maintained in good repair and working order and used for their intended purposes.

Doors and Windows
4.9 All exterior openings of buildings shall be ftted with doors or windows or other suitable means to prevent entrance of wind or rain into the building.

4.10 Windows, exterior doors, and basement or cellar hatchways shall be maintained in good repair.

4.11 Rotted or damaged doors, door frames, window frames, sashes and casings, weather-stripping, broken glass and defective door and window hardware shall be repaired and/or replaced,and maintained and protected from the elements and against decay and rust by application of a weather coating material such as paint or other protective materials.

Electrical Service
4.12 Extension cords which are not part of a fxture shall not be permitted on a semi-permanent or permanent basis.

4.13 The electrical wiring, fxtures, switches and receptacles located or used in a building shall be installed and maintained in good working order.

Exterior Walls
4.14 Exterior walls of buildings and their components including sofit and fascia shall be Maintained so as to prevent their deterioration due to weather, insects, and vegetative covering, and shall be so Maintained by painting, restoring, or Repairing the walls’ coping or fashing and by waterproofng of joints.

4.15 Where walls have been painted or otherwise treated, they shall be maintained so as to be free of peeling paint or other coatings.

Foundations
4.16 Foundation walls of a building shall be Maintained so as to prevent the entrance of insects, rodents, moisture and roots. Maintenance includes shoring of the walls, installing sub-soil drains at the footings, grouting masonry cracks, parging, damp proofng and waterproofng walls and joints and using other suitable means of Maintenance.

Grafiti
4.17 Written slogans and grafiti on the exterior of any building, wall, fence or structure shall be prohibited, including painted or chalked titles or messages with the exception of the Street Art Wall that uses the Rideaucrest retaining wall adjacent to Douglas Fluhrer Park as a designated legal wall in conjunction with the City of Kingston’s Public Art Policy.

With the exception of murals on private property as approved and sanctioned by the City of Kingston through the established application and review policy as identifed in and in conjunction with the City of Kingston’s Public Art Policy.

Guardrails (Interior & Exterior)
4.18 A guard shall be installed and maintained in good repair on the open side of any stairwell or ramp containing more than three (3) risers including the landing or a height of more than 600 mm (2 feet) between adjacent levels. A handrail shall be installed and maintained in good repair on all stairs where there are more than 3 risers or a drop of more than 600mm (2’) from the tread.

4.19 Guardrails, balustrades and handrails shall be constructed and maintained rigid in nature.Landscaping, etc.

4.20 Where landscaping, parking areas, walkways, steps, hedges, trees, fences, curbs or similar changes to a Property have been required by the City as a condition of development or redevelopment, such works shall be undertaken and Maintained so as to ensure continuous compliance with the City requirements.

Lighting
4.21 Lighting shall not be positioned so as to cause any impairment of the use or enjoyment of neighbouring properties.

Parking Areas, Walks, Driveways
4.22 All areas used for vehicular trafic and parking shall be covered with asphalt, concrete, crushed stone, paving stones arranged in an open pattern or gravel surfacing and shall be free from dirt or other litter and kept in good repair.

4.23 Entrances and means of access, excluding driveways and designated parking spaces, shall be kept clear of automobiles, trailers, motorcycles and bicycles and unsafe accumulations of ice and snow.

4.24 Walls, windows and doors separating Parking Garages from adjoining buildings, and mechanical equipment provided to exhaust fumes shall be maintained so as to prevent the accumulation of toxic fumes and the migration of toxic fumes into a building.

4.25 Steps, walks, driveways, parking spaces and similar areas shall be maintained and adequately lighted so as to aford safe passage under normal use and weather conditions.

4.26 Suitable hard surfaced walks shall be available leading from the main entrance of each dwelling to the street or driveway.

Pest Prevention
4.27 Buildings shall be kept free of rodents, vermin and insects at all times.

4.28 Basement or cellar windows used or required for ventilation and any other opening in a basement or cellar, including a foor drain, that might permit the entry of rodents, insects and vermin, shall be screened with durable material that will efectively exclude rodents, insects and vermin.

Roofs
4.29 The roof of every building shall be structurally sound, weatherproof and free of loose or unsecured objects and materials and excessive accumulations of ice and snow.

4.30 Where eaves troughs, roof gutters and/or down pipes are provided they shall be kept in good repair, including being watertight, protected by paint or other preservative and securely fastened to the building.

Signs
4.31 All signs and billboards shall be maintained in good repair and any signs which are weathered or faded or where the paint has peeled or cracked shall, with their supporting members, be removed or put into a good state of repair.

Stairs, Porches, Decks and Balconies
4.32 Inside and outside stairs, porches, decks, balconies and landings shall be maintained so as to be free of holes, cracks and other defect.

4.33 Existing stairs, treads or risers that show excessive wear or are broken, warped or loose and supporting structure members that are rotted or deteriorated shall be replaced.

4.34 All stairs, treads or risers and supporting structures shall be protected from the elements by paint or other suitable preservative.

Structural Soundness
4.35 Every part of a building, structure, pier or wharf shall be maintained in a structurally sound condition so as to be capable of sustaining its own weight and any additional load to which it may be subjected through normal use.

4.36 Walls, roofs, chimneys and other exterior parts of the building shall be free from loose or improperly secured objects or material.

4.37 Improperly secured objects and materials shall be either removed, Repaired or replaced.

4.38 Materials which have been damaged or show evidence of rot or other deterioration shall be Repaired or replaced.

Walls, Ceilings and Floors
4.39 Every wall, ceiling and foor shall be maintained so as to be free of holes, cracks, loose coverings or other defects.

4.40 The foor of every kitchen or area where food or drink is prepared and every Bathroom foor and every Toilet Room foor, where the toilet is in a separate room, shall be Maintained so as to be impervious to water and so as to permit cleaning.

4.41 All hallways, laundry rooms and common areas shall be maintained in a clean, sanitary condition.

Property, Lands, Yards and Buildings
4.42 Any furniture that is manufactured for interior use shall not be placed outside of a dwelling.

4.43 Furniture outside of a Dwelling that becomes dilapidated shall be disposed of.

4.44 Appliances including refrigerators, stoves and freezers shall not be left in yards, interior stairwells, or hallways and shall not be used as places of storage.

4.45 If a building is vacant, all water and electrical power shall be turned of other than that required for security and Maintenance of the Property.

4.46 The Owner of Vacant Property shall Maintain the Property in accordance with this Bylaw or demolish such buildings and the site left in a graded and level condition in compliance with other parts of this Bylaw.

4.47 Notwithstanding Section 4.47, Vacant Property that is located on Designated Heritage Property is subject to the requirements of Part 7 of this Bylaw.

4.48 Notwithstanding Section 4.47, Vacant Property that is located on Listed Property is subject to the requirements of Section 7.6 of this Bylaw.

4.49 All yards and compounds and lands shall be maintained in condition compatible to its intended use.

Yards, Industrial and Commercial
4.50 The warehousing of any stored material or operative equipment or the storage of garbage in receptacles in the yards or compounds shall be neat and orderly so as not to create a fre or accident hazard or any unsightly condition and shall provide clean and easy access for emergency vehicles.

4.51 Where conditions are such that a neat and orderly fashion is achieved but is still ofensive to view, the ofensive area shall be properly enclosed on all sides by solid wall or a board or metal fence 1.8 metres (6 feet) high.

Part 5 - Amenities
5.2 Amenities such as mail boxes and storage facilities shall be properly Maintained.

Basements, Cellars, and Crawlspaces
5.3 Use of a Crawl Space as a Habitable Room is prohibited.

5.4 Any Basement or Cellar used as a Dwelling Unit shall have the following requirements:

5.4.1 window area for light and ventilation shall be at least 50% above ground. Window wells are permitted if kept free of ice, snow, debris and litter;

5.4.2 foors and walls shall be impervious to water leakage;

5.4.3 Service rooms shall be separated from the remainder of the Dwelling Unit by a suitable fre separation; and

5.4.4 access to each Habitable Room shall be gained without passage through a service room.

Compost Heaps
5.5 The Occupant of a Residential Property may provide for a compost heap or bin in accordance with the health regulations, provided that the compost pile is no larger than one square metre (10 sq. ft.) and 1.8 metres (6 ft.) in height and is enclosed on all sides by concrete block, or lumber, or in a metal frame building with a concrete foor, or in a commercial plastic enclosed container designed for composting.

5.6 Compost heaps or bins shall not be placed in the front Yard or exterior side Yards.

5.7 Compost heaps or bins shall be constructed to prevent the entry of rodents or other animals, be provided with a tight ftting cover which shall be kept closed at all times except when material is being placed therein, and be maintained in a clean and sanitary condition.

Disconnected Utilities
5.8 No Owner of residential buildings or any Person or Persons acting on behalf of such Owner shall disconnect or cause to be disconnected any service or utility supplying heat, electricity, gas, refrigeration or water to a dwelling unit occupied by a tenant or lessee, except for such reasonable period of time as may be necessary for the purpose of Repairing, replacing or otherwise altering said service or utility.

Doors, Windows, and Skylights
5.9 Windows, skylights, doors and basement or Cellar hatchways shall be Maintained in good Repair, weather tight and reasonably draft-free. Maintenance includes painting, replacing damaged doors, door frames and their components, window frames, sashes and casing, replacing non-serviceable hardware, weather-stripping and re-glazing.

5.10 In a Dwelling Unit all windows and skylights intended to be opened and all exterior doors shall have hardware so as to be capable of being locked or otherwise secured from inside the Dwelling Unit without the use of keys or tools.

5.11 Where storm windows and doors are installed in a dwelling that shall be Maintained in good Repair.

5.12 All shutters on windows shall be Maintained in good Repair, including painting, replacing or other suitable means to prevent deterioration due to weather and insects.

5.13 All windows and skylights intended to be opened shall be readily operable under normally applied pressure without jamming or binding so as to perform their intended function.

5.14 All windows and skylights in a Dwelling Unit that are capable of being opened shall be ftted and equipped with screens that are Maintained in good Repair and free from defects and missing components.

5.15 Where an opening is used for illumination or ventilation and is not permanently protected by a window, skylight or door so as to exclude rodents, vermin and insects it shall be adequately screened with wire mesh or other durable material; otherwise protected so as to efectively prevent the entry of rodents, vermin and insects.

5.16 At least one entrance door in every Dwelling Unit shall have hardware so as to be capable of being locked from both inside and outside the Dwelling Unit.

5.17 Solid Core, hollow metal, or insulated steel doors shall be installed and Maintained for the entrances of Dwelling Units and hallways.

Egress
5.18 Every Dwelling and each Dwelling Unit within it shall have a continuous and unobstructed passage from the interior of the Dwelling Unit and the Dwelling to the outside of the Dwelling at street or grade level.

5.19 When an exterior staircase is used as a second means of egress, it shall be continued to ground level.

5.20 When a second means of egress requires a person or persons to travel across a roof top to reach a fre escape or a second stairwell, then a walkway complete with railing must be installed and Maintained across said roof tops.

Electrical Service
5.21 Every dwelling unit shall be wired for and provided with electricity.

5.22 Elevators intended for use by tenants shall be properly Maintained and kept in operation.

5.23 In apartment buildings where a voice communication system exists and or where a security locking and release system for the entrance is provided and is controlled from each dwelling unit such systems shall be maintained in good repair.

5.24 Every habitable room in a dwelling shall have at least one electrical duplex outlet for each 11.15 square metres (120 square feet ) of foor space, for each additional 10 square metres (100 square feet) of foor space a second duplex outlet shall be provided.

5.25 Every kitchen shall have at least two electrical duplex outlets which shall be on separate circuits.

5.26 All electrical services shall conform to and be Maintained to the regulations set by statute.

Emergency Contacts and Apartment Identifcation
5.27 Every Owner shall provide, install, and maintain contact information in a common area in case of an emergency on a 24 hour basis where an authorized person responsible for the Property can be reached.

5.27.1 In buildings having more than one Dwelling Unit, each Dwelling Unit door connected to interior common space, hallways, exits, etc. shall have the unit number posted on or beside the door and be installed in a manner and size that can be easily seen by visitors, service persons and emergency response personnel.

Garbage Disposal
5.28 Every Dwelling and every Dwelling Unit within the Dwelling shall have such receptacles as may be necessary to contain all garbage and rubbish.

5.29 Receptacles shall be:

5.29.1 constructed of a watertight material;

5.29.2 constructed to prevent the entry of rodents;

5.29.3 provided with a tight ftting cover, which shall be kept closed at all times except when garbage is being placed therein;

5.29.4 maintained in a clean and sanitary condition; and

5.29.5 located in the rear Yard of the building but shall not be placed within 3.05 metres (10’) vertically or horizontally of any opening in the structure.

5.30 Multiple Dwellings that do not have interior garbage rooms shall have Maintained and installed a receptacle large enough to contain all garbage and rubbish.

5.31 In no event shall garbage and/or garbage receptacles or recycle boxes be placed in the front yard or porch of any residential dwellings other than for immediate pick-up.

5.32 Tenants shall have daily access to garbage receptacles and garbage rooms.

5.33 Garbage and rubbish shall be stored in receptacles and removed as required by bylaw.

5.34 Receptacles shall be acceptable plastic bags or containers made of watertight construction provided with a tight ftting cover and Maintained in a clean state.

5.35 Where Repairs or cleanup require the use of bins, these bins shall be emptied when materials or debris reach the top of the bin or when odours are ofensive and may be a health hazard.

5.36 The lids to the bins shall be closed when the bins are not in use.

5.37 Accumulation or storage of garbage or refuse in public halls or stairways shall be prohibited, at all times.

General Cleanliness
5.38 Every Occupant of a Residential Property shall Maintain the Property or part thereof and the land which they occupy or control, in a clean, sanitary and safe condition and shall dispose of garbage and debris on a regular basis in accordance with municipal bylaws.

5.39 Every Occupant of a Residential Property shall Maintain every foor, wall, ceiling and fxture, under their control, including hallways, entrances, laundry rooms, utility rooms and other common areas, in a clean, sanitary and safe condition.

5.40 Accumulations or storage of garbage, refuse, appliances, or furniture in a means of egress shall not be permitted.

Heating and Heating System
5.41 Every Dwelling Unit shall be provided with a heating system capable of Maintaining a minimum temperature of 21.1C (70F).

5.42 All common areas or internal entranceways shall be provided with heating systems capable of Maintaining a minimum temperature of not less than 18 degrees C (65 degrees F).

5.43 Room temperature shall be determined at any point in the room.

5.44 Every building or part of a building which is rented or leased as Dwelling or living accommodation and which, as between the tenant or lessee and the landlord, is normally heated by or at the expense of the landlord shall, between the 15th day of September in each year and the 1st day of June of the following year, be provided with adequate and suitable heat by or at the expense of the landlord; and for the purposes of this bylaw, “adequate and suitable heat” means that the minimum temperature of the air in the accommodation which is available to the tenant or lessee is 21.1C (70F).

5.45 No residential unit shall be equipped with portable heating equipment as the primary source of heat.

5.46 Only heating equipment approved for use by a recognized standards testing authority shall be provided.

5.47 The heating system shall be Maintained in good working condition so as to be capable of heating the Dwelling safely to the standard required by this Bylaw.

5.48 All exposed pipes in habitable rooms shall be kept suficiently protected so as to prevent a safety hazard.

Kitchens
5.49 In every room in which meals can be prepared, or are prepared, there shall be installed and Maintained;

5.49.1 a suitable enclosed cupboard or shelving unit for storing food with not less than 0.226 cubic metres (8 cubic feet) of space;

5.49.2 a space provided for cooking and refrigeration appliances, including suitable electrical or gas connections for the cooking appliances;

5.49.3 work surfaces at least 1.2 metres (4 feet) in length x 60 centimeters (2 feet) in width, exclusive of the sink, that are impervious to moisture and grease and easily cleanable so as not to impart any toxic or deleterious efect to food; and

5.49.4 a sink that,
5.49.4.1 is surrounded by surfaces impervious to grease and water including at least the lower 127mm (5 inches) of the adjacent wall; and

5.49.4.2 is served with hot and cold running water.

Light
5.50 Every Habitable Room except a kitchen shall have a window or windows, skylights, translucent panels or glass area of an outside door that faces directly to outside space and admits as much natural light as would be transmitted through clear glass equal in area to fve per cent of the foor area of the room.

5.51 Public halls, common rooms, stairs, exit stairwells, porches and verandas in multiple Dwellings shall be lighted to provide a minimum level of illumination, meaning illumination of at least 50 lux (4.6 foot candle power) at all times of the day and night.

5.52 Full time lighting systems are required except during those hours when daylight sufices adequately to light the public halls.

5.53 Lighting equipment shall be provided installed and Maintained throughout to provide suficient illumination.

5.54 Every Bathroom, Toilet Room, laundry room, furnace room, Basement, Cellar or non-habitable work room and kitchen shall be provided with a permanent electrical light fxture.

Occupancy Standards
5.55 The number of Occupants residing on a permanent basis in an individual Dwelling Unit shall not exceed the maximum occupant load as prescribed by the Building Code Act, 1992, S.O. 1992, c. 23 as amended.

5.56 No room shall be used for sleeping purposes unless it has a minimum area of at least 7 square metres (75 square feet), where built in cabinets/closets are not provided, and no less than 6 square meters (65 square feet) where built in cabinets/closets are provided and no less than that required by the Ontario Building Code as amended.

Plumbing
5.57 All plumbing, including every drain, water pipe, water closet and other plumbing fxtures in a Dwelling and every connecting line to the Sewerage System shall be Maintained in good working order and free from leaks or defects, and all water pipes and appurtenances thereto shall be protected from freezing.

5.58 All plumbing fxtures shall be connected to the Sewerage System through water seal traps.

5.59 Every Dwelling shall be provided with an adequate supply of potable running water from a source approved by the Medical Oficer of Health.

5.60 All Dwellings shall have the sanitary facilities connected to a Sewerage System.

5.61 Every fxture shall be of such materials, construction and design as will ensure that the exposed surface of all parts are hard, smooth, impervious to cold or hot water, readily accessible for cleansing, and free from blemishes or cracks or other interstices that may harbour germs or impede thorough cleansing.

Toilet and Bathroom Facilities
5.62 Every wash basin, bathtub and shower shall have an Adequate supply of hot and cold running water and every water closet shall have an Adequate supply of running water.

5.63 Every Dwelling Unit (except as otherwise provided) shall contain toilet and bathroom plumbing fxtures consisting of at least one water closet, one wash basin and one bathtub or shower.

5.64 Hot water shall be so served that it may be drawn from the tap at a temperature of 43C (110F).

5.65 All Bathrooms and Toilet Rooms shall be located within and accessible from within the Dwelling Unit except that the Occupants of two Dwelling Units each containing not more than two Habitable Rooms may share toilet and bathroom facilities provided that access to the said toilet and bathroom facilities can be gained without going through rooms of either or another Dwelling Unit or outside of the building.

5.66 All Bathrooms and Toilet Rooms shall be fully enclosed.

5.67 The wash basin shall be located in the same room as the water closet, or in an immediately adjoining room.

5.68 Every Dwelling shall have at least one sink in addition to a kitchen sink.

5.69 Every Dwelling Unit shall be provided with hot and cold running water.

Ventilation
5.70 Every Habitable Room except living rooms and dining rooms shall have an opening or openings for ventilation providing an unobstructed free-fow area of at least 0.28 square meters (3 square feet) or an approved system of mechanical ventilation such that the air is changed once every hour.

5.71 All enclosed spaces including Basements, Cellars, attics or roof spaces, and Crawl Spaces shall be Adequately vented.

5.72 Where an opening is used for ventilation and is not permanently protected by a window or door so as to exclude rodents, vermin and insects it shall be:

5.72.1 Adequately screened with durable material; and

5.72.2 otherwise protected so as to efectively prevent the entry of rodents, vermin and insects.

5.73 Any openings for natural ventilation shall be protected with insect screen of corrosion-resistant material.

5.74 Every Bathroom or Toilet Room shall have an opening or openings for ventilation providing an unobstructed free-fow area of at least 0.09 square metres (1 square foot), or an equivalent such as an electric fan and a duct which shall terminate outside, shall be provided, installed and Maintained.

5.75 All mechanical ventilation systems shall be maintained in good working order.

Walls, Ceilings and Floors
5.76 Every foor, wall and ceiling in a Dwelling shall be Maintained in a clean, sanitary condition.

5.77 Every foor in a Dwelling shall be acceptably level and be Maintained so as to be free of all loose, warped, protruding, broken or rotted boards, and cracks. “Acceptably level” shall be defned as not more than 75 mm (3 inches) slope in 3 metres (10 feet) and not more than 25mm in 610 mm (1 inch in 2 feet).

5.78 Floors above an unheated space or a non-insulated Basement, Cellar, or Crawl Space shall have existing insulation Maintained.

5.79 Where necessary, interior walls shall have baseboards that shall be Maintained in good Repair and tight ftting so as to prevent the accumulation of dust and garbage.

5.80 All Bathroom walls surrounding bathtubs and showers shall be water proof and foors shall be water resistant.

Part 6 - Non-Residential Property Standards
6.1 In addition to all General Standards set out in Section 4, the following regulations shall apply to all Non-Residential Properties.

Floors
6.2 Every foor shall be smooth and level, unless otherwise designed, and Maintained so as to be free of cracks, holes and protrusions in concrete foors, also free of all loose, warped, protruding broken or rotten boards that might cause an accident or allow dirt to accumulate.

6.3 All defective foor boards shall be replaced and where foor covering has become worn or torn, the foor covering shall be Repaired, replaced or removed.

Garbage Disposal
6.4 Every building shall be provided with suficient receptacles to contain all garbage, rubbish, and trade waste.

6.5 Receptacles shall be covered at all times and shall be located in the rear Yard, when space can accommodate them, or otherwise in a side Yard, but in any event, these receptacles shall not be located in a front Yard.

6.6 Receptacles shall be placed as close to the building which they serve as is practicable but shall not be placed within 3 meters (10 feet), either vertically or horizontally, of any opening in the building.

6.7 Receptacles shall be acceptable plastic bag or other containers,

6.7.1 made of watertight construction;

6.7.2 provided with a tight ftting cover; and

6.7.3 maintained in a clean state.

6.8 Where garbage receptacles, as described above, are ofensive to view, the area where the receptacles are stored shall be enclosed on all sides by a solid masonry wall, board or metal fence that shall be 1.82 metres (6 feet) in height.

6.8.1 Such wall or fence shall contain an Adequate door or gate to allow for the removal of the garbage; and

6.8.2 All walls and fences and the doors or gates contained therein shall be Maintained in good Repair.

6.8.3 Containers shall be made available for disposal of refuse which may be discarded by customers and the lands and surrounding property shall be kept free of such refuse.

Plumbing
6.9 All plumbing, drain pipes, water pipes and plumbing fxtures in every building and every connection line to the Sewerage System shall be Maintained in good working order and free from leaks and defects and all water pipes and appurtenances thereto shall be protected from freezing.

6.10 All waste pipes shall be connected to the Sewerage System through water seal traps.

Part 7 - Additional Standards for all Designated Heritage Properties Defnitions

7.1 Despite any other provisions of this Bylaw, in this Part, “Maintenance” means routine, cyclical, non-destructive actions necessary to slow the deterioration of a Designated Heritage Property including the following: periodical inspection; Property cleanup; gardening and repair of landscape features; replacement of broken glass in windows; minor exterior repairs, including replacement of individual asphalt shingles where there is little or no change in colour or design; repainting where there is little or no change in colour; re-pointing areas of wall space under 1.5 square metres; caulking and weatherproofng; and any other work defned as maintenance in a Designation Bylaw, a Minister’s Order made pursuant to Section 34.5 of the Ontario Heritage Act, R.S.O. 1990, c.0.18, as amended, or as otherwise defned in Bylaw 2013-141, the Procedural Bylaw for Heritage, as amended.

7.2 In addition to the minimum Standards for the Maintenance and occupancy of Property set out elsewhere in this Bylaw, the Owner or Occupant of Designated Heritage Property shall:

General
a. Maintain, preserve, and protect the Heritage Attributes so as to Maintain the heritage character, visual, and structural integrity of any and all buildings, structures, or constructions located on the Property;

b. Maintain the Property in a manner that will ensure the protection and preservation of the Heritage Attributes; and

c. Comply with the provisions of Bylaw 2013-141, the Procedural Bylaw for Heritage, as amended, including obtaining a heritage permit, if required.

Every Person who contravenes any provision of this Bylaw shall, upon issuance of a Penalty Notice in accordance with the Administrative Penalty Process Bylaw 2020–69, be liable to pay to the City an Administrative Penalty as set out in Schedule B of the Administrative Penalty Process Bylaw.

Alterations to Designated Heritage Properties
7.3 Despite any other provision of this Bylaw or the Building Code Act, 1992, S.O. 1992, c. 23 as amended, no Designated Heritage Property shall be altered except as Maintenance pursuant to this

Bylaw or pursuant to the approval requirements under the Ontario Heritage Act, R.S.O. 1990, c.0.18, as amended and Bylaw 2013-141, the Procedural Bylaw for Heritage, as amended.

If a Person is required to pay an Administrative Penalty under section 7.2 in respect of a contravention of this Bylaw, the Person shall not be charged with an ofence in respect of the same contravention.

Repair of Heritage Attributes
7.4 Despite any other provision in this Bylaw, where a Heritage Attribute of a Designated Heritage Property can be Repaired, the Heritage Attribute shall not be replaced and shall be Repaired:

a. In a manner that minimizes damage to the Heritage Attribute based upon recognized national and international best practices;

b. In a manner that Maintains the design, colour, texture, grain, or other distinctive feature of the Heritage Attribute;

c. Using the same material as the original and in keeping with the design, colour, texture, grain, and any other distinctive features of the original; and

d. Where the same types of material as the original are no longer available, City-approved alternative materials that replicate the design, colour, texture, grain, or other distinctive feature, and appearance of the original material may be used in accordance with Bylaw 2013-141, the Procedural Bylaw for Heritage, as amended. In accordance with subsection 15.4.2 (2) of the Building Code Act, S.O. 1992, c. 23, if an Administrative Penalty imposed under this Bylaw is not paid within 15 days after the day that it becomes due and payable, the treasurer of the City may add the Administrative Penalty to the tax roll for any property in the City of Kingston for which all of the registered owners are responsible for paying the Administrative Penalty, and collect it in the same manner as municipal taxes.

Replacement of Heritage Attributes
7.5 Despite any other provision in this Bylaw, where a Built Heritage Specialist determines that a Heritage Attribute of a Designated Heritage Property cannot be repaired the Heritage Attribute shall be replaced:

a. Using the same types of material as the original;

b. Where the same types of material as the original are no longer available, City-approved alternative materials that replicate the design, colour, texture, grain, or other distinctive features and appearance of the original material may be used, in accordance with Bylaw 2013-141, the Procedural Bylaw for Heritage, as amended;

c. In such a manner as to replicate the design, colour, texture, grain, and other distinctive features and appearance of the Heritage Attribute; and

d. The removal of the original material shall be documented by photographs, to-scale drawings, and/or any means identifed by heritage staf.

Clearing and Leveling of Designated Heritage Properties
7.6 Despite any other provision of this Bylaw or the Building Code Act, 1992, S.O. 1992, c. 23 as amended, no building or structure located on Designated Heritage Property or on Listed Property may be altered, demolished, removed, or relocated except in accordance with the Ontario Heritage Act, R.S.O. 1990, c.0.18, as amended and Bylaw 2013-141, the Procedural Bylaw for Heritage, as amended.

Vacant Designated Heritage Properties
7.7 Despite any other provision of this Bylaw or the Building Code Act, 1992, S.O. 1992, c. 23 as amended, where a Designated Heritage Property is vacant, the Owner shall ensure that appropriate utilities serving the Property are connected, as required, in order to provide, Maintain, and to monitor proper heat and ventilation to prevent damage to the Heritage Attributes.

7.8 The Owner shall protect the Property against risk of fre, storm, inclement weather, neglect, intentional damage, or damage by other causes by efectively preventing entrance to it of all animals and unauthorized persons, and by closing and securing openings to any structures with boarding. The boarding shall be installed in such a way that minimizes damage to any Heritage Attribute, is

reversible, and minimizes visual impact.

7.9 If not already in place, an exterior lighting fxture shall be installed and/or Maintained in the front porch, veranda, or area adjacent to the front entrance of the building or structure, and must be activated by motion sensors, and shall maintain an average level of illumination of at least 50 lux at ground level.

Confict
7.10 If there is a confict between this Part and any other provision of this Bylaw or any other City Bylaw, the provision that establishes the highest standard for the protection of Heritage Attributes shall prevail.

Part 8 - Property Standards Order
8.1 An Oficer who determines that a Property does not confrm with any of the Standards prescribed in this Bylaw may issue an order pursuant to Section 15.2 of the Building Code Act, 1992, S.O. 1992, c. 23 as amended.

8.2 In accordance with Section 15.4 of the Building Code Act, 1992, S.O. 1992, c. 23 as amended, if an order made pursuant to Section 8.1 of this Bylaw is not complied with in accordance with the order as deemed confrmed or as confrmed or modifed by the Appeals Committee or a judge, the City may cause the Property to be Repaired or demolished accordingly.

8.3 The remedial work necessary to meet the requirements of this Bylaw may be undertaken by the City and the Owner will be responsible for the payment of the cost of such work, including an administrative fee as set out in Bylaw 2005-10, with the cost added to their municipal tax bill."

Part 9 - Procedures
9.1 Administration and Enforcement shall be as provided in the Building Code Act, 1992, S.O. 1992, c. 23 as amended

9.2 After the date of passing of this Bylaw, the Property Standards Committee, established under Section 5.12 of City of Kingston Bylaw 7514 continues as the Appeals Committee, the terms and conditions of which are set out in City of Kingston Committee Bylaw 2010-205, as amended from time to time.

9.3 In accordance with the provisions of Section 15.3 of the Building Code Act, 1992, S.O. 1992, c.23 as amended, an Owner or

Occupant who has been served with an order made pursuant to Section 8.1 of this Bylaw and who is not satisfed with the terms or conditions of the order may appeal to the Appeals Committee by sending a notice of appeal by registered mail together with the required administrative fee, as set out in Bylaw 2005-10, within 14 days after being served with the order."

Part 10 - Ofence and Penalty Provisions
10.1 Any Property that does not meet the Standards set out in this Bylaw shall be Repaired and Maintained to comply with the Standards of this Bylaw.

10.2 Any Person who fails to comply with an order issued under this Bylaw is guilty of an ofence and upon conviction is subject to a penalty as provided by the Building Code Act, 1992, S.O. 1992,c. 23 as amended.

10.3 If this Bylaw is contravened and a conviction entered, the Court in which the conviction was entered or any Court of competent jurisdiction may, in addition to any other remedy, and to any penalty that is imposed, make an order prohibiting the continuation or repetition of the ofence by the person convicted.

Part 11 - Validity
11.1 If a Court of competent jurisdiction declares any provision, or any part of a provision, of this Bylaw to be invalid, or to be of no force and efect, it is the intention of Council in enacting this Bylaw that each and every provision of this Bylaw authorized by law be applied and enforced in accordance with its terms to the extent possible according to law.

11.2 Where a provision of this Bylaw conficts with the provision of another Bylaw in force in the City, the provisions that establish the higher Standards to protect the health, safety and welfare of the general public prevails.

Part 12 - Commencement
12.1 This Bylaw shall come into force and take efect on the date of its passing.

12.2 After the date of passing of this Bylaw, Bylaw 8597 continues to apply to Properties in respect of which an order has been issued prior to the date of passing of this Bylaw, and then only to such properties until such time as the work required by such order has been completed or any enforcement proceedings in respect of such order, including demolition and Repair by the City, have been concluded."

"""


PROMPT_TEMPLATE = """
You are an AI assistant representing the City of Kingston, Ontario. Your role is to provide accurate, well-structured, and legally compliant answers regarding local bylaws, rules, and regulations.

### **Guidelines for Answering:**
1️⃣ **Understand and Interpret User Intent**:  
   - Analyze the user's question in plain language and determine which bylaw or regulation applies.  
   - If multiple bylaws could be relevant, prioritize the most applicable one.

2️⃣ **Use Only Provided Context**:  
   - Answer **only** using the information retrieved from the Kingston bylaws dataset.  
   - If the information is **not available**, respond with:  
     _"I'm sorry, but I couldn't find this information in my records. You may check [Kingston's official website](https://www.cityofkingston.ca/) for more details."_

3️⃣ **Match User Queries to the Right Bylaw Category**:  
   - **Noise Bylaw (2004-52)** → Questions about loud music, construction noise, quiet hours, etc.  
   - **Water Regulation Bylaw (2006-122)** → Questions about water restrictions, conservation, usage rules, etc.  
   - **Property Standards Bylaw** → Questions about landlord obligations, property maintenance, tenant rights, etc.  
   - **Nuisance Parties Bylaw** → Questions about large gatherings, fines for rowdy behavior, etc.  
   - **Tree Bylaw** → Questions about tree removal, permits, and conservation rules.  

4️⃣ **Provide a Clear & Concise Response**:  
   - Always **cite the relevant bylaw** when answering. Example:  
     - _"According to the Noise Bylaw (2004-52), loud music is not permitted past 11 PM."_  
     - _"According to the Water Regulation Bylaw (2006-122), external water use is restricted during summer months."_  
     - _"According to the Property Standards Bylaw, landlords must maintain rental properties to a specific standard."_  
   - Keep responses **brief, informative, and to the point** without unnecessary details.  

---
### **Extracted Bylaws for Reference:**
🔍 **Context (Laws & Regulations Extracted from the Dataset):**  
{context}
    
❓ **User Question:**       
{question}

💡 **Answer in a Clear & Concise Manner:**
"""

# Regulatory Chatbot Class
class RegulatoryChatbot:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0.7)
        self.chat_prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    def process_query(self, query_text: str):
        """Process user query."""
        try:
            if "water" in query_text.lower():
                local_context = WATER_REGULATION_TEXT
                regulation_name = "Water Regulation Bylaw (2006-122)"
            else:
                local_context = NOISE_REGULATION_TEXT
                regulation_name = "Noise Bylaw (2004-52)"

            response = self.llm.invoke(
                self.chat_prompt.format(
                    context=local_context,
                    question=query_text
                )
            ).content

            return f"According to the {regulation_name}, {response}"

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return f"Error: {str(e)}"

# Initialize the chatbot
chatbot = RegulatoryChatbot()

st.title("City of Kingston Regulatory Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_query = st.text_input("You:", key="user_input")
if st.button("Send"):
    if user_query:
        response = chatbot.process_query(user_query)
        st.session_state.chat_history.append(("You", user_query))
        st.session_state.chat_history.append(("Bot", response))
    else:
        st.warning("Please enter a query.")

# Display chat history (Most Recent First)
st.write("## Chat History")
for role, text in reversed(st.session_state.chat_history):  # Reverse the list before displaying
    st.write(f"**{role}:** {text}")
