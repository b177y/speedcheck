#!/bin/bash

SPEEDCHECK_PATH=`pwd`

if [ "$EUID" -ne 0 ]
  then
  echo -e "\nThis script needs to be run as root. Aborting. \n"
  exit 1
fi

if ! [ -x "$(command -v speedtest)" ]; then
  echo 'Error: speedtest is not installed.' >&2
  exit 1
fi

if ! [ -x "$(command -v python3)" ]; then
  echo 'Error: python3 is not installed.' >&2
  exit 1
fi

python3 -m pip install -r requirements.txt

echo -e "#!/bin/bash\ncd /home/billy/speedcheck\n/usr/bin/python3 code/run-test.py && /usr/bin/python3 code/graph.py" > /usr/local/bin/speedcheck
chmod +x /usr/local/bin/speedcheck

(crontab -l 2>/dev/null; echo "*/10 * * * * /usr/local/bin/speedcheck") | crontab -