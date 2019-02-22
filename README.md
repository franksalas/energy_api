
# EIA Open Data [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/franksalas/energy_api.git/master)
U.S Energy Information Administration API data extraction.


Currently, EIA's API contains the following main data sets:

- Hourly electricity operating data, including actual and forecast demand, net generation, and the power flowing between electric systems
- 408,000 electricity series organized into 29,000 categories
- 30,000 State Energy Data System series organized into 600 categories
- 115,052 petroleum series and associated categories
- 34,790 U.S. crude imports series and associated categories
- 11,989 natural gas series and associated categories
- 132,331 coal series and associated categories
- 3,872 Short-Term Energy Outlook series and associated categories
- 368,466 Annual Energy Outlook series and associated categories
- 92,836 International energy series

# Enviroment
Clone repo & `cd`  to project folder

```bash
git clone https://github.com/franksalas/energy_api.git

cd energy_api
```
Create enviroment fro `.yml` file

```bash
conda env create -f enviroment.yml
```
Activate enviroment
```bash
source activate energy_api
```
