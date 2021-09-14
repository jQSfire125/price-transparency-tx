## Hospital Price Transparency (Texas)

The Centers for Medicare and Medicaid Services recently required hospitals under  [45 CFR §180.50](https://www.federalregister.gov/d/2019-24931/p-1010) to publish a [list of prices](https://www.cms.gov/hospital-price-transparency) on their websites.  They specifically instruct hospitals to make these lists:

- As a comprehensive machine-readable file with all items and services.   
- In a display of shoppable services in a consumer-friendly format.  

There is a lot of variation in adherence to these policies.  Without strong guidance on formatting from CMS, hospitals are all over the map on formatting.  Many hospitals have complied with the new rules but in ways that are not consumer friendly.  

**This repository cuts out pricing noise purposefully introduced by these hospital systems**.  You can easily search for a given CPT or HCPCS code and compare those prices across hospitals.  

### Acknowledgments

This work is based on the work of **Nathan Sutton**. He started a repository for price transparency in North Carolina. You can find his repository [here][nategit].

### Ontology

We rely on the excellent work of the [Athena](https://athena.ohdsi.org/) vocabulary to define the ontology of healthcare procedures.  This maps [CPT](https://www.ama-assn.org/practice-management/cpt) and [HCPCS](https://www.cms.gov/Medicare/Coding/MedHCPCSGenInfo) codes into a [common data model](https://github.com/OHDSI/CommonDataModel).

### Coverage

This repository covers hospitals in the Austin/San Antonio TX and sourrouding counties. Coverage of North Carolina can be found in this [repository][nategit]

### Usage

Quickstart with docker-compose
```
docker-compose up
```

Run the flyway migrations
```
docker-compose run flyway
```

Run the ETL
```
docker-compose run etl
```

Interactive PSQL client
```
docker exec -it postgres psql -d postgres -U builder
```

### Contact

Submit an issue if you find anything inconsistent.  Like all data products, we make no assumptions and provide no warrantee.  

[nategit]: https://github.com/nathansutton/hospital-price-transparency