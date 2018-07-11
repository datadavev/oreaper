oreaper
=======

Parse ORE documents from DataONE to produce a map of relations. Output is a 
series of JSON records, one per line.

::
  usage: oreaper [-h] [-l] [-x DATE_START] [-y DATE_END] [-b BASE_URL]
               [-C MAX_RECORDS] [-p PAGE_SIZE] [-s START_INDEX]

  Load DataONE ORE documents and output relations as a json dictionary, one entry per line.

  optional arguments:
    -h, --help            show this help message and exit
    -l, --log_level       Set logging level, multiples for more detailed.
    -x DATE_START, --date_start DATE_START
                          Starting time for listing
    -y DATE_END, --date_end DATE_END
                          End time for listing
    -b BASE_URL, --base_url BASE_URL
                          Baseurl for listObjects (https://cn.dataone.org/cn)
    -C MAX_RECORDS, --max_records MAX_RECORDS
                          Maximum number of entries to retrieve.
    -p PAGE_SIZE, --page_size PAGE_SIZE
                          Page size to return
    -s START_INDEX, --start_index START_INDEX
                          Zero based index of first entry

Example::

  $ oreaper
  {"metadata_pids": ["dcx_0007f892-0d8f-4451-94e9-94d02ba5dd0d_0"], "resource_map_pids": ["0007f892-0d8f-4451-94e9-94d02ba5dd0d_0"], "data_pids": ["iso19139_0007f892-0d8f-4451-94e9-94d02ba5dd0d_0"]}
  {"metadata_pids": ["dcx_0007f892-0d8f-4451-94e9-94d02ba5dd0d_1"], "resource_map_pids": ["0007f892-0d8f-4451-94e9-94d02ba5dd0d_1"], "data_pids": ["iso19139_0007f892-0d8f-4451-94e9-94d02ba5dd0d_1"]}
  ...
  {"metadata_pids": ["dcx_0024e77f-000e-4b38-8a80-215fab398905_2"], "resource_map_pids": ["0024e77f-000e-4b38-8a80-215fab398905_2"], "data_pids": ["iso19139_0024e77f-000e-4b38-8a80-215fab398905_2"]}
  {"metadata_pids": ["00327229-485e-4865-a8d2-eb33d27438af-snotel_201606_1017.xml"], "resource_map_pids": ["00327229-485e-4865-a8d2-eb33d27438af-snotel_201606_1017.rdf"], "data_pids": ["00327229-485e-4865-a8d2-eb33d27438af-snotel_201606_1017.zip"]}


