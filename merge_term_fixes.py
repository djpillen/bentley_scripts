import csv

unid_terms_fix_final = 'C:/Users/Public/Documents/unidentified_terms_fix.csv'
unid_terms_fix_1 = 'C:/Users/Public/Documents/unidentified_terms_fix_1.csv'
unid_terms_fix_2 = 'C:/Users/Public/Documents/unidentified_terms_fix_2.csv'

multi_terms_fix_final = 'C:/Users/Public/Documents/multiple_type_terms_fix.csv'
multi_terms_fix_1 = 'C:/Users/Public/Documents/multiple_type_terms_fix_1.csv'
multi_terms_fix_2 = 'C:/Users/Public/Documents/multiple_type_terms_fix_2.csv'

def merge_csvs(start_csv, final_csv):
    with open(start_csv,'rb') as csvfile:
        reader = csv.reader(csvfile)
        next(reader,None)
        for row in reader:
            with open(final_csv,'ab') as csvout:
                writer = csv.writer(csvout)
                writer.writerow(row)

merge_csvs(unid_terms_fix_1,unid_terms_fix_final)
merge_csvs(unid_terms_fix_2,unid_terms_fix_final)
merge_csvs(multi_terms_fix_1,multi_terms_fix_final)
merge_csvs(multi_terms_fix_2,multi_terms_fix_final)
