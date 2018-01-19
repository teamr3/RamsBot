
task main()
{
	while (true){
		motor[port2] = vexRT[Ch2]*0.7;
		motor[port3] = vexRT[Ch2]*0.7;
		motor[port4] = vexRT[Ch3]*0.7;
		motor[port5] = vexRT[Ch3]*0.7;
		motor[port6] = vexRT[Btn8D]*127;
		motor[port6] = -vexRT[Btn8U]*127;
		motor[port7] = vexRT[Btn7D]*127*0.1;
		motor[port8] = vexRT[Btn7D]*127*0.1;
	}
}
