RED='\033[0;31m'
NC='\033[0m'

if ./mu cc.m | grep -q generated
then
    make cc
    ./cc -tf -m181960 > trace.t
    ./cc -m181960
else
    printf "${RED}ERROR!!!\n${NC}"
    printf "${RED}ERROR MSG:${NC}"
    ./mu cc.m
    printf "${RED}ERROR!!!\n${NC}"
fi