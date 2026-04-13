<img width="579" height="93" alt="image" src="https://github.com/user-attachments/assets/4d4f9c79-294d-4a9b-8989-b1cbfc979db4" />

### There were 2 files in the archive:
#### encoder.py — the main Python script with the logic of the task.
#### output.txt — a file with the already generated encryption results.

#### What was important in encoder.py:
variable e = 7

function RSA_enc(plain_text)

function get_flag_bits(flag)

#### calculation:
enc_seed = pow(seed, e, n)
writing to the file:

seed = ...

flag = ...

### What was in output.txt:

large number seed = ...

encrypted/scrambled flag in hex: flag = a9fa3c5e51d4cea498554399848ad14aa0764e15a6a2110b6613f5dc87fa70f17fafbba7eb5a2a5179

### How is the seed formed

#### Explain:

I_LOVE_RNG is converted to a number

this number is encrypted with RSA

the result becomes the seed

then the seed is encrypted again with enc_seed

### How is the flag encrypted

#### Explain:

the flag is converted to bits

the bits are shuffled 10 times
for each step random.seed(seed * (i + 1)) is used

so if you restore the seed, you can repeat the permutations


In the task, we were given an archive with a Python script where the message and flag are shuffled using `random.shuffle`, and RSA is used to generate the seed.
At first glance, it seems that we need to break RSA, but in fact the implementation is vulnerable because the message is very small and there is no padding.
The goal is to recover the seed, and then undo the bit shuffling back.

