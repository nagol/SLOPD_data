
import urllib.request
import re
import csv
from datetime import date

def parse_slopd_report(verbose = False, save_raw = False):
    try:

        today = date.today()

        # get the SLOPD data
        with urllib.request.urlopen('https://pdreport.slocity.org/policelog/rpcdsum.txt') as f:
            text = f.read().decode('utf-8')

        # save a copy for inspecting if parser is working correctly
        if save_raw:
            with open(f"data/raw_files/SLOPD_report_{today}.txt", 'w', newline='\n') as f:
                f.write(text)

    except urllib.error.URLError as e:
        print(e.reason)

    try:

        report_counter = 0     # Keep track of number of police reports parsed
        extracted_cases = {}   # Container for data, indexed by report number
        SEPARATOR = '==============================================================================='
        
        for chunk_num, chunk_text in enumerate(text.split(SEPARATOR)):

            # Each police report is of the pattern ==/header/==/body
            if chunk_num > 0:

                    if chunk_num % 2 == 1:

                        report_counter += 1
                        if verbose:
                            print(f'Processing header for report number {report_counter} \n{"-"*40}\n{chunk_text}')

                        #                             210819016 08/19/21         Received:08:11 Dispatched:      Arrived:08:12 Cleared:08:12
                        header_pattern = re.compile("(\d{9}) (\d{2}/\d{2}/\d{2}) Received:(.*?) Dispatched:(.*?) Arrived:(.*?) Cleared:(.*?)")
                        report_header_matches = header_pattern.search(chunk_text)

                        extracted_cases[report_counter] = {
                            'case_number': report_header_matches.group(1),
                            'date': report_header_matches.group(2),
                            'received': report_header_matches.group(3).strip(),
                            'dispatched': report_header_matches.group(4).strip(),
                            'arrived': report_header_matches.group(5).strip(),
                            'cleared': report_header_matches.group(6).strip()
                        }
                        

                    if chunk_num % 2 == 0:
                        if verbose:
                            print(f"Processing body text for report {report_counter}")
                            print('-' * 40)

                        observed_crime_flag = False

                        for _num, _text in enumerate(chunk_text.split('\n')):

                            if _text == '':
                                continue

                            type_pattern = re.compile("Type: (.*?)  Location:([A-Z]{1,3}[0-9]{1,3})")
                            type_pattern_matches = type_pattern.search(_text)
                            if type_pattern_matches:
                                extracted_cases[report_counter]['type'] = type_pattern_matches.group(1).strip()
                                extracted_cases[report_counter]['grid_location'] = type_pattern_matches.group(2).strip()

                            location_pattern = re.compile("Addr: (.*) GRID (.*) Clearance Code:(.*)")
                            location_pattern_matches = location_pattern.search(_text)
                            if location_pattern_matches:
                                observed_crime_flag = False
                                extracted_cases[report_counter]['address'] = location_pattern_matches.group(1).strip()
                                extracted_cases[report_counter]['location'] = location_pattern_matches.group(2).strip()
                                extracted_cases[report_counter]['clearance_code'] = location_pattern_matches.group(3).strip()
                                extracted_cases[report_counter]['observed_crime'] = observed_crime.strip()

                            if 'As Observed:' in _text.strip() and not observed_crime_flag:
                                observed_crime = _text.strip().replace("As Observed:", "") 
                                observed_crime_flag = True

                            if observed_crime_flag:
                                observed_crime = observed_crime.replace("As Observed:", "")  + _text.strip().replace("As Observed:", "")  

                            resp_officer_pattern = re.compile("Responsible Officer: (.*)")
                            resp_officer_pattern_matches = resp_officer_pattern.search(_text)
                            if resp_officer_pattern_matches:
                                extracted_cases[report_counter]['responsible_officer'] = resp_officer_pattern_matches.group(1).strip()

                            units_pattern = re.compile("Units: (.*)")
                            units_pattern_matches = units_pattern.search(_text)
                            if units_pattern_matches:
                                extracted_cases[report_counter]['units'] = units_pattern_matches.group(1).replace(' ', '')

                            des_pattern = re.compile("Des: (.*)")
                            des_pattern_matches = des_pattern.search(_text)
                            if des_pattern_matches:
                                extracted_cases[report_counter]['description'] = des_pattern_matches.group(1).strip()

                            cc_pattern = re.compile("CALL COMMENTS: (.*)")
                            cc_pattern_matches = cc_pattern.search(_text)
                            if cc_pattern_matches:
                                extracted_cases[report_counter]['call_comments'] = cc_pattern_matches.group(1).strip()

                        
    except Exception as e:
        print("Something bad happended...")
        print(e)


    finally:

        for key, value in extracted_cases.items():
            if verbose:
                print()
                print(f'For report number {key}:')

            for key_report, value_report in value.items():
                if verbose:
                    print(f'     {key_report}: {"-"*(30 - len(key_report))}-> {value_report}')

        with open('data/csv/SLOPD_report.csv', 'a', newline='') as csvfile:

            datawriter = csv.DictWriter(
                csvfile, 
                fieldnames=[
                    'case_number',
                    'date',
                    'received',
                    'dispatched',
                    'arrived',
                    'cleared',
                    'type',
                    'grid_location',
                    'location',
                    'address',
                    'observed_crime',
                    'responsible_officer',
                    'units',
                    'description',
                    'call_comments',
                    'clearance_code'
                ]
            )

            for key, value in extracted_cases.items():
                datawriter.writerow(value)

            if verbose:
                print(f'There were {max(extracted_cases.keys())} reports captured...')
            
            

parse_slopd_report(verbose = False)      
                
