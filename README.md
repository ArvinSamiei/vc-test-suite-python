## Files that are within the repository

This repository contains a script(valid_vc_generator.py) for generating Verifiable credentials that abide by normative statements provided by the W3c data model 1.1 & 2.0 specification.This ensures that all the required attributes with a chosen set of arbitrary one are combined.It also contains a validator script(maximus_validator.py) that takes .json files in a seperate directory for checking whether a credential abides by the normative statements provided by the W3C Verifiable credential data model 1.1 & 2.0 specification. Their is also a report pdf(Report_DTLab.pdf) providing further clarification on the functionality of the two scripts along with a greater context of the purposes of these scripts. Their are also existing test suites that are used within this repository. The validator utilizes the test suites that either abide or violate the normative statements for w3c data model 1.1 which can be found in dtt-test-api/tests_scripts/input. Their are test suites within the repository tht abide or violate the normative statements for w3c data model 2.0 which can be found in tests/input.

## Regarding the options for the Validator script
Their are three options 


## Getting started

For generating verifiable credentials:
```bash
python3 valid_vc_generator.py
```

Example output of generating verifiable credentials:
```bash
•generating attribute VerifiableCredential
 •generating attribute credentialSubject
  ◦['http://1edtech.edu/credentials/3732', {'id': 'http://1edtech.edu/credentials/3732'}] assigned to credentialSubject
 •generating attribute issuer
  ◦['http://1edtech.edu/credentials/3732', {'id': 'http://1edtech.edu/credentials/3732'}] assigned to issuer
 •generating attribute id
  ◦['http://1edtech.edu/credentials/3732', {'id': 'http://1edtech.edu/credentials/3732'}] assigned to id
 •generating attribute type
  ◦None assigned to type
 •generating attribute credentialSchema
  •generating attribute type
   ◦random-string assigned to type
  •generating attribute id
   ◦http://1edtech.edu/credentials/3732 assigned to id
  ◦[{'type': 'random-string', 'id': 'http://1edtech.edu/credentials/3732'}] assigned to credentialSchema
 •generating attribute credentialStatus
  ◦[{'type': 'https://www.w3.org/ns/credentials/status#BitstringStatusListCredential'}] assigned to credentialStatus
 •generating attribute description
  ◦None assigned to description
 •generating attribute evidence
  •generating attribute type
   ◦random-string assigned to type
  ◦[{'type': 'random-string'}] assigned to evidence
 •generating attribute validFrom
  ◦['2024-08-30T14:05:54Z'] assigned to validFrom
 •generating attribute validUntil
  ◦['2024-08-30T14:05:54Z'] assigned to validUntil
 •generating attribute name
  ◦None assigned to name
 •generating attribute proof
  •generating attribute type
   ◦random-string assigned to type
  ◦[{'type': 'random-string'}] assigned to proof
 •generating attribute refreshService
  •generating attribute id
   ◦http://1edtech.edu/credentials/3732 assigned to id
  •generating attribute type
   ◦random-string assigned to type
  ◦[{'id': 'http://1edtech.edu/credentials/3732', 'type': 'random-string'}] assigned to refreshService
 •generating attribute termsOfUse
  •generating attribute type
   ◦random-string assigned to type
  ◦[{'type': 'random-string'}] assigned to termsOfUse
 •generating attribute confidenceMethod
  ◦['http://1edtech.edu/credentials/3732', {'id': 'http://1edtech.edu/credentials/3732'}] assigned to confidenceMethod
 •generating attribute relatedResource
  ◦['http://1edtech.edu/credentials/3732', {'id': 'http://1edtech.edu/credentials/3732'}] assigned to relatedResource
```

For validating Verifiable credentials
```bash
python3 maximus_validator.py
```

Example results of valid
```bash

```