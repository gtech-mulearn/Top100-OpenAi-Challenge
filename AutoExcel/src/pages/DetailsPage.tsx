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
              context
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
    <div className='p-7'>
    <h1>Enter data to insert after configuring settings</h1>
    
    <DialogDemo/>
    <Label htmlFor='unstructured'></Label>
    <Input id="unstructured" className='mr-25 my-5' value={data} placeholder='enter your data' onChange={e=>{setData(e.target.value)}}/>
    <Button className='mx-7' onClick={handleOnClick}>
        send
    </Button>
    </div>
    </>
}