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


## Recovering the seed

After computing the exact integer 49th root of `enc_seed`, we recover the original message:

`b'I_LOVE_RNG'`

Once `m` is known, the seed is easy to reconstruct:

`seed = m^7`

At this point, we have exactly the same seed that was used by the challenge script.


## Reversing the bit shuffling

Recovering the seed is only the first part of the solution.  
The next step is to undo the repeated `random.shuffle()` operations applied to the flag bits.

Since the flag bits were shuffled 10 times, we must:
1. reproduce the same shuffle for each round,
2. build the inverse permutation,
3. apply the inverse permutations in reverse order.

This works because Python's shuffle is deterministic when the seed is known.

So for each round, we recreate the shuffled index order, then use it to move every bit back to its original position.



## Full solve script

The script (solve.py)below:
1. recovers the original message from `enc_seed`,
2. reconstructs the seed,
3. reverses all shuffle operations,
4. converts the recovered bitstream back into bytes,
5. prints the final flag.





