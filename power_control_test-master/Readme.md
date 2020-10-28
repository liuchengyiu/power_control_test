bin config:<br/>
    mkdir test in $HOME<br/>
    cp bin to $HOME/test <br/>

test config: <br/>
performance:<br/>
    type: <br/>
        cpu_frequence<br/>
    param:<br/>
        average: 100 // Mhz<br/>
        single: 100 // Mhz<br/>

    type: <br/>
        emmc_speed<br/>
    param:<br/>
        speed: 100 // Gb
    
    type: <br/>
        ram_speed<br/>
    param:<br/>
        speed: 100 // Gb
    
hardware:<br/>
    type:<br/>
        eth_speed<br/>
    param:<br/>
        serverip: 192.168.1.122 <br/>
        speed: 100 // Mb/s <br/>

stress:<br/>
    type:<br/>
        cpu_stress<br/>
    param:<br/>
        time: 100 // second<br/>

    type:<br/>
        ram_stress<br/>
    param:<br/>
        num: 100 // process num<br/>
        size: 1G // malloc size<br/>
        release_time: 100s // release ram interval<br/>
        last_time: 10000 // test time<br/>

