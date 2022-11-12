jpose = get_joint_position()
temp_state = jpose[5]
jpose[5] = temp_state + 90
joint_ptp(jpose,100,100,0.0)
jpose[5] = temp_state
joint_ptp(jpose,100,100,0.0)
