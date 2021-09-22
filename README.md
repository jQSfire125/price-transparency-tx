## Hospital Price Transparency (Texas)

 

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