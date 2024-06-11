from spotify_driver import Driver

playlists = {
    '37i9dQZF1E36NxxSFMMnUd':'Daily Mix 1',
    '37i9dQZF1E37dNHWKzvmmI':'Daily Mix 2',
    '37i9dQZF1E35ZooVC8Ul8v':'Daily Mix 3',
    '37i9dQZF1E3ac8jzjuqGB5':'Daily Mix 4',
    '37i9dQZF1E3672iwSX3DgE':'Daily Mix 5',
    '37i9dQZF1E375FraRp5Z3B':'Daily Mix 6',
    
    '37i9dQZF1EVJHK7Q1TBABQ':'Upbeat Mix',
    '37i9dQZF1EVHGWrwldPRtj':'Chill Mix',
    '37i9dQZF1EVJSvZp5AOML2':'Happy Mix',
    '37i9dQZF1EVKuMoAJjoTIw':'Moody Mix',
    '37i9dQZF1EVGJJ3r00UGAt':'Romantic Mix',
    '37i9dQZF1EIdzRg9sDFEY3':'Party Mix',
    '37i9dQZF1EIhxsZ1zwdwMW':'Morning Mix',
    '37i9dQZF1EIhMasSPCl82r':'Afternoon Mix',
    '37i9dQZF1EIe9sVvozltCh':'Evening Mix',
    '37i9dQZF1EIfBND9ikx3Yp':'Late Night Mix',

    '37i9dQZF1EQnqst5TRi17F':'Hip Hop Mix',
    '37i9dQZF1EQqkOPvHGajmW':'Indie Mix', 
    '37i9dQZF1EQmPV0vrce2QZ':'Country Mix',
    '37i9dQZF1EQpj7X7UK8OOF':'Rock Mix',
    '37i9dQZF1EQp9BVPsNVof1':'Dance/Electronic Mix',
    '37i9dQZF1EQncLwOalG3K7':'Pop Mix',
    '37i9dQZF1EQntZpEGgfBif':'Soul Mix',
    '37i9dQZF1EQp62d3Dl7ECY':'Folk & Acoustic Mix',
    '37i9dQZF1EQoqCH7BwIYb7':'R&B Mix',

    '37i9dQZF1EIe64niGyd0Ng':'Monday Mix',
    '37i9dQZF1EIcvJYW3RDbOu':'Tuesday Mix',
    '37i9dQZF1EIgdZz2klOuWo':'Thursday Mix',
    '37i9dQZF1EIgrk7FqBoeuz':'Friday Mix',
    '37i9dQZF1EIgxk3CRmRMU3':'Saturday Mix',
    '37i9dQZF1EIf89LJGA0yiU':'Sunday Mix',
    '37i9dQZF1EIdb9OVCqWxy9':'Weekday Mix'
}

driver = Driver('postgresql://postgres:Pc!!308182!!@localhost/spotify', 'df44137dd8bc4671ab03ca53b89a405b', 'a6102acbe1254eb686234e7eb8bdde3f')

driver.update_all_playlists()