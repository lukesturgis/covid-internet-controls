# covid-internet-controls

This respository serves as the basis for all content related to the hunt for COVID-19 censorship detection.


## Worker

Each VPS that is used for gathering data is classified as a `worker`.

To learn more, read `worker/README.md`.

## Ansible

For configuration management, Ansible is used in order to secure each host and deploy the latest software changes.

To learn more, read `ansible/README.md`.


## Testing

This project utilizes `pytest` for performing all code testing.

To run these tests, first install `pytest`:

    pip install pytest

Then run the tests:

    pytest
