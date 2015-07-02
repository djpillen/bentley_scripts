## Things to do

These are things that we either are or will be continuously working on in the ongoing effort to clean up our legacy metadata for migration to ASpace
* Marc_xml
    1. Extents
    2. Subjects
    3. Agents
    4. Merging instances of 'papers', 'visual materials', etc. for the same collection
    5. Identifying things that actually shouldn't go to ASpace (after we determine what those are)
    6. ...pretty much everything else we did for EADs
* Accessions
    1. Accession dates (normalization and figure out what to do about undated accessions)
    2. Donors
* EAD
    1. Subject/agent authority ids
    2. Compound subjects
    3. Extents (?)
* General
    1. Locations?

## Things to save until (just before) we're ready to migrate

These are the things that we have the ability to do at any time, but should save until just before we're ready to migrate because they make potentially significant and problematic (for DLXS) changes to the EADs or because they rely on using for-real ASpace URIs.

* Containers
    1. Run container_parent_ids to add 'id' attributes to each top level container and 'parent' attributes to child Containers
    2. Run container_barcodes to add "barcodes" to top containers
* Subjects and agents
    1. Import unique subjects and agents and insert the URI for each into the relevant places in our EADs/marc_xml/accessions and also modify the ASpace imported to look for the uri and link the resources/accessions to the subjects/agents
