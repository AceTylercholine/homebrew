# Homebrew
Various scripts I've written

## Analyzers

Some scripts I wrote to analyze data. Not the scripts used for final data analysis.

## Extractors

GoNoGo_Processor.py & MID_Processor.py used to extract relevant data from EPrime data files and export the results to a csv.

Stroop_Processor.py used to extract relevant data from PsychoPy data files (.csv format) and export results to a new csv.

## Figure-Scripts

Some scripts I wrote to visualize specific data results. Not the scripts used to make final figures.

## MATLAB_Stroop

Color word Stroop program I made in a MATLAB class. Learning MATLAB helped me learn :snake:, and although I now prefer Python, I am fairly comfortable switching between them.
> [!WARNING]
> Functional, but barely

## Home Dir Files

### fdr3.m
MATLAB function to provide False Discovery Rate corrected p-values using the Benjamini-Hochberg procedure

Looks like:
```MATLAB
function [fdrArrayOrgOrder] = fdr3(pvals)

    % Determine input shape
    isRow = isrow(pvals);
    originalSize = size(pvals); %store for reshaping later

    % Find nans
    nanIndices = isnan(pvals);
    validPvals = pvals(~nanIndices);

    % Calculate FDR on valid p-values
    correctedValidPvals = fdr_no_nans(validPvals); % See helper function below

    % Reconstruct the output array
    fdrArrayOrgOrder = NaN(originalSize); % Initialize with NaNs
    % Fill in the non-nan values
    fdrArrayOrgOrder(~nanIndices) = correctedValidPvals;

    function [fdrArrayOrgOrder] = fdr_no_nans(pvals)

        pvalsLen = length(pvals);

        % Reshape to row vector for processing
        pvals = reshape(pvals, 1, []);
        % Sort p-values and store original indices
        [pvalsSort, pvalsI] = sort(pvals);

        % Initialize the array to store FDR corrected p-values
        fdrArray = zeros(1, pvalsLen);

        % Initialize previous FDR for monotonicity enforcement
        prevFDR = 1;

        % Iterate through p-values from largest to smallest
        for i = pvalsLen:-1:1
            pVal = pvalsSort(i);
            pValRank = i; % The rank of the current p-value (1-based index)

            % Calculate the FDR corrected p-value
            fdr_pval = pVal * (pvalsLen / pValRank);

            % Enforce monotonicity: corrected p-value should not be greater than the previous one
            fdr_pval = min(fdr_pval, prevFDR);

            % Store the corrected p-value
            fdrArray(i) = fdr_pval;

            % Update the previous FDR value
            prevFDR = fdr_pval;
        end

        % Restore the original order of the corrected p-values
        [~, inv_pvalsI] = sort(pvalsI);
        fdrArrayOrgOrder = fdrArray(inv_pvalsI);
    end
end
```

### remove_begin_nums.py
I had a folder with a ton of files named '[#] [name].[ext]' and wanted to get rid of the numbers and space at the beginning of the name. Some names might've been duplicated with the numbers already removed, so this script removes those duplicates and continuously removes the first character of the each file's name until it's a letter

Looks like:
```python
import os

files = os.listdir()

for filename in files:
    if filename[0] != '.' and len(filename) > 1:
        while filename[0].isalpha() == False:
            if os.path.isfile(filename[1:]):
                os.remove(filename[1:])
            else:
                os.rename(filename, filename[1:])
                filename = filename[1:]
```

### shuffle_num_list.py
Creates a .txt of a range of numbers shuffled. Useful for creating a document to pull random subject ID's from.

The script contains two functions and variables with default min and max of 100 & 999. Edit these numbers before running the script:
```python
start_num = 100
end_num = 999
```
