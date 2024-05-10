import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import { Card } from 'primereact/card';
import { Dialog } from 'primereact/dialog';
import { Button } from 'primereact/button';
import { ProgressBar } from 'primereact/progressbar';
import 'primereact/resources/themes/saga-blue/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';

function App() {
    const [latestEntries, setLatestEntries] = useState([]);
    const [showAbout, setShowAbout] = useState(false);

    useEffect(() => {
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

    const getLatestEntryPerDevice = (entries) => {
        const latestByDevice = {};
        entries.forEach(entry => {
            const deviceId = entry.deviceId;
            if (!latestByDevice[deviceId] || latestByDevice[deviceId].timestamp < entry.timestamp) {
                latestByDevice[deviceId] = entry;
            }
        });
        return latestByDevice;
    };

    const runScript = () => {
        console.log('Executing /network_monitoring_backend/snmp_collector.py');
    };

    const sidebarContent = (
        <div className="p-d-flex p-flex-column" style={{gap: '1rem', backgroundColor: '#f4f4f4', height: '100vh', padding: '2rem'}}>
            <Button label="SNMP Update" className="p-button-lg" onClick={runScript} />
            <Button label="About" className="p-button-lg" onClick={() => setShowAbout(true)} />
            
        </div>
    );

    const aboutDialog = (
        <Dialog header="About" visible={showAbout} modal onHide={() => setShowAbout(false)} breakpoints={{'960px': '75vw', '640px': '100vw'}} style={{width: '50vw'}}>
            <p>System Usage Dashboard</p>
            <p>Version: 1</p>
        </Dialog>
    );

    return (
        <div className="p-grid">
            <div className="p-col-fixed" style={{width: '250px'}}>
                {sidebarContent}
            </div>
            <div className="p-col">
                {aboutDialog}
                <div className="p-grid p-justify-start" style={{ margin: '20px', gap: '20px' }}>
                    {latestEntries.map((entry, index) => (
                        <div className="p-col-fixed" style={{width: '300px'}} key={index}>
                            <Card title={`Device ${entry.device_name}`} style={{ textAlign: 'center' }}>
                                <div className="p-d-flex p-flex-column p-ai-center">
                                    <h5>CPU Usage</h5>
                                    <ProgressBar value={entry.cpu_usage} showValue={false} style={{width: '100%', marginBottom: '1rem'}} />
                                    <div style={{width: '100%', marginBottom: '1rem'}} className="p-d-flex p-jc-between">
                                        
                                        <span>{entry.cpu_usage}%</span>
                                        
                                    </div>
                                    <h5>RAM Usage</h5>
                                    <ProgressBar value={entry.ram_usage} showValue={false} style={{width: '100%', marginBottom: '1rem'}} />
                                    <div style={{width: '100%'}} className="p-d-flex p-jc-between">
                                        
                                        <span>{entry.ram_usage}%</span>
                                        
                                    </div>
                                </div>
                            </Card>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default App;