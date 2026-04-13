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




In the task, we were given an archive with a Python script where the message and flag are shuffled using `random.shuffle`, and RSA is used to generate the seed.
At first glance, it seems that we need to break RSA, but in fact the implementation is vulnerable because the message is very small and there is no padding.
The goal is to recover the seed, and then undo the bit shuffling back.

