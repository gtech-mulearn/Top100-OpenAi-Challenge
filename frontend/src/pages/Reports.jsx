import React, { useEffect, useState } from 'react';
import NavBar from '../components/NavBar';
import axios from 'axios';

function Reports() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:4003/reports')
      .then((res) => {
        setData(res.data);
      

        const medical_report= res.data[0].report
        //split this string as array 
        const medical_report_array = medical_report.split('\n')
        console.log(medical_report_array)
      })
      .catch((err) => {
        console.log('Error fetching data:', err);
        setData([]); // Reset data to an empty array or handle error state
      });
  }, []);

  return (
    <main>
      <NavBar />
      <div className='text-white m-5 p-5'>
        <h1 className=' text-blue-200 font-bold m-10'>Medical Report </h1>
        {/* <p>{data && data[0]?.report}</p> */}

     
        {data && data[data.length -1 ]?.report.split('\n').map((item, index) => (
          <p key={index}>{item}</p>
        ))}
     
      </div>
    </main>
  );
}

export default Reports;
