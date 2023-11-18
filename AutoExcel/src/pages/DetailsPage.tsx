import React from 'react';

import { useNavigate } from "react-router-dom"
import { Button } from "semantic-ui-react";


import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogClose
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import  { useState } from 'react'

export function DialogDemo() {
    const [sheet,setSheet] = useState('')
    const [context,setContext] = useState('')
    const [columns,setColumns] = useState('')
    function onSubmit(){
        localStorage.setItem('context',context)
        localStorage.setItem('sheet',sheet)
        localStorage.setItem('columns',columns)
        
    }

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline" className='absolute top-3 right-3'>Settings</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Setup App Config</DialogTitle>
          <DialogDescription>
            Make changes to your app details here.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="name" className="text-right">
              Sheet Name
            </Label>
            <Input
              id="name"
              onChange={e=>{setSheet(e.target.value)}}
              value={sheet}
            placeholder='enter your sheet name'
              className="col-span-3"
            />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="context" className="text-right">
              context
            </Label>
            <Input
            
                onChange={e=>{setContext(e.target.value)}} value={context}
              id="context"
              placeholder='enter you use case'
              className="col-span-3"
            />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="columns" className="text-right">
              columns
            </Label>
            <Input
            onChange={e=>{setColumns(e.target.value)}} value={columns}
              id="columns"
              placeholder="enter your columns"
              className="col-span-3"
            />
          </div>
        </div>
        <DialogFooter>
        <DialogClose asChild>
          <Button onClick={onSubmit} type="submit">Save changes</Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}


export function DetailsPage(){



    const [data,setData] = useState('')
    const nav  = useNavigate();

    function handleOnClick(){
        console.log(localStorage.getItem('context'))
        fetch('http://localhost:8000/openai', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            data: data,
            context: localStorage.getItem('context'),
            columns: localStorage.getItem('columns')
        })
    })  
        .then(response => {
            console.log(response.body)
            return response.json()})
        .then(result => {

            fetch('http://localhost:8000/addrow/'+localStorage.getItem('sheet'), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    ...result
                })
            }).then(()=>setData("")) 
        })
        .catch(error => {
            // handle errors here
            console.error(error);
        });
        
    }  
    
    return <>
    <div className='bg-black text-white'>
    <div className='bg-black text-white h-screen flex-col place-between'>
    <div className='flex p-4 grow bg-gray-900'><h1>AutoEntry</h1></div> 
    
 
    <div className=" p-7 leading-relaxed h-auto text-gray-300 text-[19px] flex-col overscroll:hidden grow-[1] ">
      
      <div className='flex-col grow-[1] h-full'>
      <h1>Steps to Setup AutoEntry</h1>
      1.<span className='pr-1'></span> Create a new spread sheet. (take care that name of spread sheet has no spaces)<br/>
      2.<span className='pr-1'></span> Give editor access to given mail autoexcelserviceaccount@autoexcel-405401.iam.gserviceaccount.com<br/>
      3.<span className='pr-1'></span> Use the setting button on top right of the screen to set the configuration<br/>
      3.<span className='pr-1'></span> Now give a small context for your business using context ".....".<br/>
      4.<span className='pr-1'></span> Give the columns of excel sheet in order using columns ".....".<br/>
      5.<span className='pr-1'></span> Set sheet name using sheet "..."<br/>
      6.<span className='pr-1'></span> Now you can send unsorted data to the bot and it will be sorted and added to the sheet.
  
      </div>
      <div className='flex text-gray-300 mt-[300px] grow m-2'><Input className='bg-black' type="text" onChange={e=>setData(e.target.value)} />
      <button className=' ml-3 text-lg px-5 rounded bg-gray-900 text-white hover:outline outline-2 p-2' onClick={handleOnClick}>send</button>
      </div>
      </div>
      
    <DialogDemo/>
    
    
    </div>
    </div>
    </>
}