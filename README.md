Python Pipedrive API
====================

The project provides access to the Pipedrive API

The project is still at an early stage and requires a lot of testing. Any help including bug reports is appreciated.

### Usage:

    from pypipedrive import PipeDrive
    p = PipeDrive("YOUR_API_KEY")
    print p.persons()
    print p.persons.find(term="Persons Name")
    print p.persons(method='POST', name='Ivanov I.I.')
    print p.persons._id(method='DELETE', _id=1)

