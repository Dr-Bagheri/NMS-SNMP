import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import { Typography, Row, Col, Card } from 'antd';

function App() {
    const [latestEntries, setLatestEntries] = useState([]);

    useEffect(() => {
        const getLatestEntryPerDevice = (entries) => {
            const latestByDevice = {};
            entries.forEach(entry => {
                // Assuming each entry has an 'id' and a 'timestamp'
                const deviceId = entry.deviceId;
                if (!latestByDevice[deviceId] || latestByDevice[deviceId].timestamp < entry.timestamp) {
                    latestByDevice[deviceId] = entry;
                }
            });
            return latestByDevice;
        };

        const fetchData = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/data/');
                const entries = response.data;
                const latestPerDevice = getLatestEntryPerDevice(entries);
                setLatestEntries(Object.values(latestPerDevice));
            } catch (error) {
                console.log("Error fetching data:", error);
            }
        };

        fetchData();
    }, []);

    return (
        <div style={{ padding: '20px' }}>
            <Typography.Title level={2}>System Usage Dashboard</Typography.Title>
            <Row gutter={16}>
                {latestEntries.map((entry, index) => (
                    <React.Fragment key={index}>
                        <Col span={12}>
                            <Card title={`Device ${entry.deviceId} - CPU Usage`}>
                                <CircularProgressbar
                                    value={entry.cpuUsage}
                                    text={`${entry.cpuUsage}%`}
                                    styles={buildStyles({
                                        textColor: 'blue',
                                        pathColor: 'turquoise',
                                    })}
                                />
                            </Card>
                        </Col>
                        <Col span={12}>
                            <Card title={`Device ${entry.deviceId} - RAM Usage`}>
                                <CircularProgressbar
                                    value={entry.ramUsage}
                                    text={`${entry.ramUsage}%`}
                                    styles={buildStyles({
                                        textColor: 'blue',
                                        pathColor: 'turquoise',
                                    })}
                                />
                            </Card>
                        </Col>
                    </React.Fragment>
                ))}
            </Row>
        </div>
    );
}

export default App;