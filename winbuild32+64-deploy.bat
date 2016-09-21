py -3.4 release_prep.py
py -3.4 omnitool/database.py > omnitool/database.txt
py -3.4 omnitool/Resources/resourcepack.py
py -3.4-32 omnisetup.py build
py -3.4 omnisetup.py build
iscc setup.iss
iscc setup64.iss
@pause