# Eggs Over Easy

## Description

In this challenge, I was given a file that did not contain any visible text at first glance. After inspecting it more carefully, I noticed that the file consisted only of two types of whitespace characters: `space` and `tab`.

Because there were only two possible symbols, I assumed that the file was using binary encoding. I mapped the characters as follows:

- `space = 0`
- `tab = 1`

## Solution

I converted the full sequence of spaces and tabs into a bitstring using that mapping. Then I split the bitstring into groups of 8 bits and converted each group into its ASCII representation.

This produced the following intermediate result:

```text
ff35 ff24 ff23 ff34 46 ff5b ff22 ff14 ff43 ff4f ff4e ff5d
```

This was not the final flag yet, but it clearly looked like a sequence of hexadecimal Unicode code points. Most of the values started with `FF`, which is common for fullwidth Unicode characters.

After converting each hexadecimal value into its Unicode character, I obtained:

```text
ＵＤＣＴF｛Ｂ４ｃｏｎ｝
```

At this point, it became clear that the text was written mostly with fullwidth Unicode symbols instead of standard ASCII characters. By applying Unicode normalization (`NFKC`), those fullwidth symbols were converted into normal ASCII text.

The final decoded flag was:

```text
UDCTF{B4con}
```

## Hint Analysis

The challenge hint said:

> If you know what goes well with eggs, this will be over easily...

This points to **bacon**, which matches the last part of the decoded flag and confirms that the solution is correct.

## Flag

```text
UDCTF{B4con}
```
