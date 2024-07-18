
// Chakra imports
import {
	Box,
	Button,
	CircularProgress,
	CircularProgressLabel,
	Flex,
	Grid,
	Icon,
	Progress,
	SimpleGrid,
	Spacer,
	Stack,
	Stat,
	StatHelpText,
	StatLabel,
	StatNumber,
	Table,
	Tbody,
	Text,
	Th,
	Thead,
	Tr
} from '@chakra-ui/react';
// Styles for the circular progressbar
import medusa from 'assets/img/cardimgfree.png';
// Custom components
import Card from 'components/Card/Card.js';
import CardBody from 'components/Card/CardBody.js';
import CardHeader from 'components/Card/CardHeader.js';
import BarChart from 'components/Charts/BarChart';
import LineChart from 'components/Charts/LineChart';
import IconBox from 'components/Icons/IconBox';
// Icons
import { CartIcon, DocumentIcon, GlobeIcon, RocketIcon, StatsIcon, WalletIcon } from 'components/Icons/Icons.js';
import DashboardTableRow from 'components/Tables/DashboardTableRow';
import TimelineRow from 'components/Tables/TimelineRow';

import { AiFillCheckCircle } from 'react-icons/ai';
import { BiHappy } from 'react-icons/bi';
import { BsArrowRight } from 'react-icons/bs';
import { IoCheckmarkDoneCircleSharp, IoEllipsisHorizontal } from 'react-icons/io5';
// Data
import {
	barChartDataDashboard,
	barChartOptionsDashboard,
	lineChartDataDashboard,
	lineChartOptionsDashboard
} from 'variables/charts';
import { dashboardTableData, timelineData } from 'variables/general';
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Dashboard() {
    const [snmpData, setSnmpData] = useState({
		device_name: '',
		cpu_usage: 0,
		ram_usage: 0,
		timestamp: '',
	    anomaly: 0,
	});

    useEffect(() => {
        // Update the wsUrl to match your Django server's WebSocket route
        const wsUrl = 'ws://localhost:8000/ws/snmp/';
        const ws = new WebSocket(wsUrl);

        ws.onopen = () => {
            console.log("WebSocket connection established.");
        };

        ws.onmessage = (event) => {
			const receivedData = JSON.parse(event.data);
  
			// Updating state with the SNMP data
			setSnmpData(receivedData.message);
		};

        // Cleanup function to close WebSocket connection when the component unmounts
        return () => {
            ws.close();
        };
    }, []);
	
	return (
		<Flex flexDirection='column' pt={{ base: '120px', md: '75px' }}>
			<SimpleGrid spacing='24px'>
				
				<Card>
				
					<CardBody>
						<Flex flexDirection='row' align='center' justify='center' w='100%'>
							<Stat me='auto'>
								<StatLabel fontSize='sm' color='gray.400' fontWeight='bold' pb='2px'>
									Anamoly Detection by AI
								</StatLabel>
								<Flex>
									
									{snmpData.predicted_label === 0 ? (	
									<StatHelpText
										alignSelf='flex-end'
										justifySelf='flex-end'
										m='0px'
										color='green.400'
										fontSize='30px'
										fontWeight='bold'
										fontSize='md'>
										NO Anomaly Detected &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Anomaly type : Normal&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;RAM Usage : {snmpData.hrStorageUsed.toFixed(2)}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;            CPU Usage : {snmpData.hrProcessorLoad.toFixed(2)}
									</StatHelpText> 
                                    ) : (
									<StatHelpText
										alignSelf='flex-end'
										justifySelf='flex-end'
										m='0px'
										color='red.400'
										fontWeight='bold'
										fontSize='38px'
										fontSize='md'>
										Anomaly Detected &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Anomaly type : {snmpData.anomaly_type}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;RAM Usage : {snmpData.hrStorageUsed.toFixed(2)}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;           CPU Usage : {snmpData.hrProcessorLoad.toFixed(2)}
									</StatHelpText>
								    )}
									

								</Flex>
							</Stat>
							<IconBox as='box' h={'45px'} w={'45px'} bg='brand.200'>
								<WalletIcon h={'24px'} w={'24px'} color='#fff' />
							</IconBox>
						</Flex>
					</CardBody>
				</Card>
				{/* MiniStatistics Card */}
				
			</SimpleGrid>
			<Grid templateColumns={{ sm: '1fr', md: '1fr 1fr ', '2xl': '2fr 1.3fr 1.3fr' }} my='26px' gap='18px'>
				{/* Welcome Card */}
				<Card
					p='0px'
					gridArea={{ md: '1 / 1 / 2 / 3', '2xl': 'auto' }}
					bgImage={medusa}
					bgSize='cover'
					bgPosition='50%'>
					<CardBody w='100%' h='100%'>
						<Flex flexDirection={{ sm: 'column', lg: 'row' }} w='100%' h='100%'>
							<Flex flexDirection='column' h='100%' p='22px' minW='60%' lineHeight='1.6'>
								<Text fontSize='sm' color='gray.400' fontWeight='bold'>
									Welcome back,
								</Text>
								<Text fontSize='28px' color='#fff' fontWeight='bold' mb='18px'>
									Thomas & Tech team
								</Text>
								<Text fontSize='md' color='gray.400' fontWeight='normal' mb='auto'>
									Glad to see you again! <br />
									Ask me anything.
								</Text>
								<Spacer />
								<Flex align='center'>
									<Button
										p='0px'
										variant='no-hover'
										bg='transparent'
										my={{ sm: '1.5rem', lg: '0px' }}>
										<Text
											fontSize='sm'
											color='#fff'
											fontWeight='bold'
											cursor='pointer'
											transition='all .3s ease'
											my={{ sm: '1.5rem', lg: '0px' }}
											_hover={{ me: '4px' }}>
											Tab to record
										</Text>
										<Icon
											as={BsArrowRight}
											w='20px'
											h='20px'
											color='#fff'
											fontSize='2xl'
											transition='all .3s ease'
											mx='.3rem'
											cursor='pointer'
											pt='4px'
											_hover={{ transform: 'translateX(20%)' }}
										/>
									</Button>
								</Flex>
							</Flex>
						</Flex>
					</CardBody>
				</Card>
				<Card gridArea={{ md: '2 / 1 / 3 / 2', '2xl': 'auto' }}>
					<CardHeader mb='24px'>
						<Flex direction='column'>
							<Text color='#fff' fontSize='lg' fontWeight='bold' mb='4px'>
								Performance
							</Text>
							<Text color='gray.400' fontSize='sm'>
								Ram Usage
							</Text>
						</Flex>
					</CardHeader>
					<Flex direction='column' justify='center' align='center'>
						<Box zIndex='-1'>
							<CircularProgress
								size={200}
								value={snmpData.hrStorageUsed.toFixed(2)}
								thickness={6}
								color='#582CFF'
								variant='vision'
								rounded>
								<CircularProgressLabel>
									<IconBox mb='20px' mx='auto' bg='brand.200' borderRadius='50%' w='48px' h='48px'>
									
									</IconBox>
								</CircularProgressLabel>
							</CircularProgress>
						</Box>
						<Stack
							direction='row'
							spacing={{ sm: '42px', md: '68px' }}
							justify='center'
							maxW={{ sm: '270px', md: '300px', lg: '100%' }}
							mx={{ sm: 'auto', md: '0px' }}
							p='18px 22px'
							bg='linear-gradient(126.97deg, rgb(6, 11, 40) 28.26%, rgba(10, 14, 35) 91.2%)'
							borderRadius='20px'
							position='absolute'
							bottom='5%'>
							<Text fontSize='xs' color='gray.400'>
								0%
							</Text>
							<Flex direction='column' align='center' minW='80px'>
								<Text color='#fff' fontSize='28px' fontWeight='bold'>
									{snmpData.hrStorageUsed.toFixed(2)}%
								</Text>
								<Text fontSize='xs' color='gray.400'>
									Based on SNMP data
								</Text>
							</Flex>
							<Text fontSize='xs' color='gray.400'>
								100%
							</Text>
						</Stack>
					</Flex>
				</Card>
				<Card gridArea={{ md: '2 / 2 / 3 / 2', '2xl': 'auto' }}>
					<CardHeader mb='24px'>
						<Flex direction='column'>
							<Text color='#fff' fontSize='lg' fontWeight='bold' mb='4px'>
								Performance
							</Text>
							<Text color='gray.400' fontSize='sm'>
								Cpu Usage
							</Text>
						</Flex>
					</CardHeader>
					<Flex direction='column' justify='center' align='center'>
						<Box zIndex='-1'>
							<CircularProgress
								size={200}
								value={snmpData.hrProcessorLoad.toFixed(2)}
								thickness={6}
								color='#582CFF'
								variant='vision'
								rounded>
								<CircularProgressLabel>
									<IconBox mb='20px' mx='auto' bg='brand.200' borderRadius='50%' w='48px' h='48px'>
									
									</IconBox>
								</CircularProgressLabel>
							</CircularProgress>
						</Box>
						<Stack
							direction='row'
							spacing={{ sm: '42px', md: '68px' }}
							justify='center'
							maxW={{ sm: '270px', md: '300px', lg: '100%' }}
							mx={{ sm: 'auto', md: '0px' }}
							p='18px 22px'
							bg='linear-gradient(126.97deg, rgb(6, 11, 40) 28.26%, rgba(10, 14, 35) 91.2%)'
							borderRadius='20px'
							position='absolute'
							bottom='5%'>
							<Text fontSize='xs' color='gray.400'>
								0%
							</Text>
							<Flex direction='column' align='center' minW='80px'>
								<Text color='#fff' fontSize='28px' fontWeight='bold'>
							 	{snmpData.hrProcessorLoad.toFixed(2)}%
								</Text>
								<Text fontSize='xs' color='gray.400'>
									Based on SNMP data
								</Text>
							</Flex>
							<Text fontSize='xs' color='gray.400'>
								100%
							</Text>
						</Stack>
					</Flex>
				</Card>
			</Grid>
			
			<Grid templateColumns={{ sm: '1fr', md: '1fr 1fr', lg: '2fr 1fr' }} gap='24px'>
				{/* Projects */}
				<Card p='16px' overflowX={{ sm: 'scroll', xl: 'hidden' }}>
					<CardHeader p='12px 0px 28px 0px'>
						<Flex direction='column'>
							<Text fontSize='lg' color='#fff' fontWeight='bold' pb='8px'>
								Tasks
							</Text>
							<Flex align='center'>
								<Icon as={IoCheckmarkDoneCircleSharp} color='teal.300' w={4} h={4} pe='3px' />
								<Text fontSize='sm' color='gray.400' fontWeight='normal'>
									<Text fontWeight='bold' as='span'>
										10 done
									</Text>{' '}
									this month.
								</Text>
							</Flex>
						</Flex>
					</CardHeader>
					<Table variant='simple' color='#fff'>
						<Thead>
							<Tr my='.8rem' ps='0px'>
								<Th
									ps='0px'
									color='gray.400'
									fontFamily='Plus Jakarta Display'
									borderBottomColor='#56577A'>
									Task
								</Th>
								<Th color='gray.400' fontFamily='Plus Jakarta Display' borderBottomColor='#56577A'>
									Members
								</Th>
								<Th color='gray.400' fontFamily='Plus Jakarta Display' borderBottomColor='#56577A'>
									Budget
								</Th>
								<Th color='gray.400' fontFamily='Plus Jakarta Display' borderBottomColor='#56577A'>
									Completion
								</Th>
							</Tr>
						</Thead>
						<Tbody>
							{dashboardTableData.map((row, index, arr) => {
								return (
									<DashboardTableRow
										name={row.name}
										logo={row.logo}
										members={row.members}
										budget={row.budget}
										progression={row.progression}
										lastItem={index === arr.length - 1 ? true : false}
									/>
								);
							})}
						</Tbody>
					</Table>
				</Card>
				{/* Orders Overview */}
				<Card>
					<CardHeader mb='32px'>
						<Flex direction='column'>
							<Text fontSize='lg' color='#fff' fontWeight='bold' mb='6px'>
								Future Questions Coverage
							</Text>
							<Flex align='center'>
								<Icon as={AiFillCheckCircle} color='green.500' w='15px' h='15px' me='5px' />
								<Text fontSize='sm' color='gray.400' fontWeight='normal'>
									<Text fontWeight='bold' as='span' color='gray.400'>
	                                +91%
									</Text>{' '}
									AI Accuracy
								</Text>
							</Flex>
						</Flex>
					</CardHeader>
					<CardBody>
						<Flex direction='column' lineHeight='21px'>
							{timelineData.map((row, index, arr) => {
								return (
									<TimelineRow
										logo={row.logo}
										title={row.title}
										date={row.date}
										color={row.color}
										index={index}
										arrLength={arr.length}
									/>
								);
							})}
						</Flex>
					</CardBody>
				</Card>
			</Grid>
		</Flex>
	);
}

export default Dashboard;