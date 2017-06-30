#!/bin/bash
echo -e '\e[93mWelcome to the RAMSBOT setup wizard'
echo -e '\e[0mThis tool will guide you through the installation proccess for the RAMSBOT development workspace'

function info() {
	echo -e -n '\e[0;1;35m[*] \e[0m'
	echo $1
}

function procedure() {
	echo -e -n '\e[0;1;35m[.] \e[0m'
	echo -n $1
}

function end() {
	echo -e '\e[93mdone!\r\e[0;1;35m[*'
}

function important() {
	echo -e -n '\e[0;1;93m[!] \e[0m'
	echo $1
}

function enderror() {
	echo -e '\e[31merror!\r\e[0;1;35m[!'
}

function prompt() {
	echo -e -n '\e[0;1;35m[>] \e[0m'
}

procedure 'doing preinstall checks... '

# verify we are in the scripts directory
if [[ $PWD != */scripts ]]; then
	enderror
	important "You need to run this script from within the scripts directory!"
	exit 1
fi

# verify ros is installed
if hash roscore 2>/dev/null; then
	:
else
	enderror
	important "I couldn't detect a roscore. Please ensure ros is installed and can be found"
	exit 1
fi

# try to create log file
touch setuplog.txt
echo "ramsbot installer start" > setuplog.txt
if [ $? -ne 0 ]; then
	enderror
	important "I couldn't create my log file."
	exit 1
fi

LOG_PATH=$(readlink -f setuplog.txt)

sleep 1
end

info 'ready to install, press enter to continue'
read

pushd . > /dev/null
cd ../rosws

procedure 'initializing ros workspace... '
if [ -f .catkin_workspace ]; then
	enderror
	important "there's already a ros workspace here. aborting."
	exit 2
fi

echo 'init catkin workspace' >> $LOG_PATH
catkin_init_workspace src >> $LOG_PATH
if [ $? -ne 0 ]; then
	enderror
	important "couldn't create ros workspace. see log for details"
	exit 2
fi

end

popd
info 'now ready to install dependencies'
info 'the following dep scripts were found:'
info 'name | description'
info '-----+------------'
for filename in deps/*.sh; do
	echo -e -n '\e[0;1;93m[|] \e[0m '
	echo -n $(basename "$filename" .sh)
	echo -n ' | '
	echo $(awk 'FNR==3{print substr($0,3)}' $filename)
done

info 'please choose one'
while true; do
	prompt
	read DEPSCRIPT
	DEPSCRIPT_FILE=deps/$DEPSCRIPT.sh
	if [ -f $DEPSCRIPT_FILE ]; then
		chmod +x $DEPSCRIPT_FILE
		break
	else
		important 'that depscript does not exist'
	fi
done

info 'now installing dependenices'
$DEPSCRIPT_FILE

info 'done'

pushd . > /dev/null
cd ../rosws

procedure 'running build... '
echo 'running build' >> $LOG_PATH
catkin_make >> $LOG_PATH
if [ $? -ne 0 ]; then
	enderror
	important "couldn't build! see log for details"
	exit 2
fi

end

popd
info "Installation complete!"
info "Do you want to see the readme now?"
info "Well too bad. Go look at it on your own time"
exit 0
