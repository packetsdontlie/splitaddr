# Address Problems

Given that address1, address2, city, state, zip have different loci of control, matching addresses is pretty hard.

* Zip - is it zip or zip + 4
* State - is it CA, Cali, Ca., California
* Address1 - is it 123 State Street or 123 NW State St
* Address2 - is it Ste 3000 or Suite 3000

# Address Decomposition

What if a small language model could make everything discrete?

```
source_addressnumber         | 4700
source_streetname            | Hale
source_placename             | Denver
source_statename             | CO
source_zipcode               | 80220
source_occupancytype         | Suite
source_occupancyidentifier   | 200
```

# Tools

* t5addr.py - uses HuggingFace T5
* flanaddr.py - uses Google T5 Flan

# Environment

You'll need a properly configure venv for python
