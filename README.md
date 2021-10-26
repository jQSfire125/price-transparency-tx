## Hospital Price Transparency (Texas)

 ![Big Data Ecosystem](https://media.npr.org/assets/img/2015/04/29/stagnes-exterior_wide-f590399293a2e93233700cfef9ddbafd4f873edd.jpg?s=600)

### 1. Motivation 
The Centers for Medicare and Medicaid Services (**CMMS**) require hospitals to publish a list of prices on their websites. Hospitals publish the files in different formats and with differing breakdowns of their prices. In most cases, the file is not easily accessible. It takes some searching to find them and the files usually are not consumer-friendly.

This repository aimed to gather the data for all hospitals in the Austin/San Antonio TX region, transform it into a standard format and framework, and load it into a PostgreSQL database. Once there, we were able to analyze which hospital was the best relative value in different scenarios. That analysis is in `Analysis.ipynb`

### 1.1 Source Data

The first step was to compile a list of the hospitals in the Austin/San Antonio, TX area. The table with the listing of all hospitals is in `/volumes/data/dim`.

The next step was to visit each site and download the available files to comply with the CMMS ruling. You can find those raw files in `/volumes/data/raw`.

### 1.2 Ontology

Hospitals use different codings to publish their prices. We rely on the excellent work of the [Athena](https://athena.ohdsi.org/) vocabulary to define the ontology of healthcare procedures. This maps [CPT](https://www.ama-assn.org/practice-management/cpt) and [HCPCS](https://www.cms.gov/Medicare/Coding/MedHCPCSGenInfo) codes into a [common data model](https://github.com/OHDSI/CommonDataModel).

The disadvantage with this normalization is that we exclude the hospital-specific items such as their room and board charges, for example.

### 1.3 Transformation

The docker files in the repository run ETL transformations on the raw files, normalize the data and load it into a Postgres database. 

The hospitals include different types of prices. The four groups included in our analysis are:
* **gross**: The "list" price for a procedure. Hospitals typically never actually charge at this rate. 
* **cash**: The self-pay discounted price one would pay without insurance.
* **max**: The maximum negotiated rate by an insurance company in the hospital's network.
* **min**: The minimum negotiated rate by an insurance company in the hospital's network.

Most hospitals reported the de-identified maximum and minimum negotiated prices. A minority of them also included each insurance company's payer and plan-specific charges, but those are not in this version of the analysis.

### 1.4 Usage

Quickstart with docker-compose:  
`docker-compose up`

Run the flyway migrations:  
`docker-compose run flyway`

Run the ETL:  
`docker-compose run etl`

Interactive PostgreSQL client:  
`docker exec -it postgres psql -d postgres -U builder`

### Acknowledgements
This repository is based on the work of **Nathan Sutton**. He started a repository for price transparency of hospitals in North Carolina. You can find his repository [here](https://github.com/nathansutton/hospital-price-transparency). Nate is also my mentor.

### Contact

Submit an issue if you find anything inconsistent.  Like all data products, we make no assumptions and provide no warrantee.

[nategit]: https://github.com/nathansutton/hospital-price-transparency