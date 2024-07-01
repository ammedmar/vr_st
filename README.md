# VR_ST

## Authors
TBW

## Abstract

TBW

## Bibliography: technical aspects 
This project uses the package biblatex to handle the bibliography, therefore it needs biber as the bibliography tool, instead of bibtex. Additionally, it is suggested that all bib entries include a DOI and/or URL. 
## Suggested LaTeX practices

1. Use `\colon` instead of `:` for defining functions.

2. Use `\mid` for sets or group presentations. For example, `\set{a \in A \mid a=b}` is superior to `\set{a \in A | a=b}`.

3. Leave space around most operators. For example, `f \colon X \to Y` is superior to `f:X\to Y`. Possible exceptions are guided by readability, for example:

   ```latex
   \begin{equation}
       \sum_{i=1}^n = \frac{n(n+1)}{2}.
   \end{equation}
   ```

4. No punctuation inside math mode. Use `$a+b$,` instead of `$a+b,$`.

5. No line breaks in the middle of sentences.

6. Use line breaks at the end of each sentences.

7. No double blank spaces or trailing blank spaces.

8. Use tab instead of blank spaces for indentation.

9. All named environments with the possible exception of `document` should be tabbed. For example,

   ```latex
   \begin{lemma*}
       Statement.
   \end{lemma*}
   ```

10. Do not use `$$...$$` for display equations; instead, use one of the environments in the AMS display equation family or

    ```latex
    \[
    \]
    ```

11. Leave a blank line before and after most environments. Possible exceptions are AMS display equation family.

12. Leave a blank line before and after sections and subsections.

13. Unless a there is a good reason not to, use `\dots` instead of either `\ldots` or `\cdots` or others. The `amsmath` package uses nearby operators to choose the right type of dots for `\dots`.