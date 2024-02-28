import React, { useState, useEffect } from "react";
import {
  Box,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  Typography,
  Tooltip,
  IconButton,
  TooltipProps,
  tooltipClasses,
} from "@mui/material";
import { Slider, FormControlLabel, Switch } from '@mui/material';
import { padding, styled } from "@mui/system";
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
type MessageType = {
  text: string;
  type: "user" | "assistant";
};

const MAX_CHARACTERS = 4000;

const CustomWidthTooltip = styled(({ className, ...props }: TooltipProps) => (
  <Tooltip {...props} classes={{ popper: className }} />
))({
  [`& .${tooltipClasses.tooltip}`]: {
    maxWidth: 200,
  },
});

const ChatComponent: React.FC = () => {
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [newMessage, setNewMessage] = useState<string>("");

//These are so that the selected option in dropdown stays mounted
// These are send to backend to configure pipeline
  const [llms, setllms] = useState<string>('GPT 3.5 Turbo 0125');
  const [retrievalStrategies, setRetrievalStrategies] = useState<string>('Hybrid Search');
  const [disableSelectIndex, setDisableSelectIndex] = useState<boolean>(false);
  const [openSearchIndices, setOpenSearchIndices] = useState<string>('voyage-2-large');

//These are to catch the currently selected dropdown choice
  const handleDropDownChange_llm = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setllms(event.target.value);
  };

  const handleDropdownChange_retrieval = (event: React.ChangeEvent<HTMLSelectElement>) => {
    if(event.target.value == "Sparse Retrieval"){
      setDisableSelectIndex(true)
    }
    else{setDisableSelectIndex(false)}
    setRetrievalStrategies(event.target.value);
  };
  const handleDropdownChange_index = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setOpenSearchIndices(event.target.value);
  };

  //These are for the api requests - load the options on the dropdown menue with the returned lists
  const [llms_list, setllms_list] = useState<[]>([]);
  const [retrievalStrategies_list, setRetrievalStrategies_list] = useState<[]>([]);
  const [openSearchIndices_list, setOpenSearchIndices_list] = useState<[]>([]);

  // For citation slider
  const [citationActive, setCitationActive] = useState(true);

  // Function to toggle visibility of advanced mode
  const [showBox, setShowBox] = useState(false); // Initial state: hidden
  
  const AdvancedMode = () => {
    //When Advanced mode is activated remove default values, if deactivated 
    if(showBox == false){
      setOpenSearchIndices("")
      setRetrievalStrategies("")
      setllms("")
    }
    if(showBox == true){
      setOpenSearchIndices("voyage-2-large")
      setRetrievalStrategies("Hybrid Search")
      setllms("GPT 3.5 Turbo 0125")
    }
    
    setShowBox(!showBox);
  };

// Query available pipeline config when page loads for the first time
  useEffect(() => {
    const requestIndices = new Request("http://127.0.0.1:8000/getOpenSearchIndices", {
      method: "GET",
    });
    async function getIndicies(this: any){
      try{
        console.log("calling")
        const response = await fetch(requestIndices);
        const data = await response.json();
        setOpenSearchIndices_list(data)
      }
      catch(error){
        console.log(error)
  
      }
    }
    const requestLLm = new Request("http://127.0.0.1:8000/getLLMs", {
      method: "GET",
    });
    async function getLLMs(this: any){
      try{
        console.log("calling")
        const response = await fetch(requestLLm);
        const data = await response.json();
        setllms_list(data)
      }
      catch(error){
        console.log(error)
  
      }
    }
    const requestRetrievalStrategy = new Request("http://127.0.0.1:8000/getRetrievalStrategy", {
      method: "GET",
    });
    async function getRetrievalStrategy(this: any){
      try{
        console.log("calling")
        const response = await fetch(requestRetrievalStrategy);
        const data = await response.json();
        setRetrievalStrategies_list(data)
      }
      catch(error){
        console.log(error)
  
      }
    }
    getIndicies()
    getLLMs()
    getRetrievalStrategy()

  }, []); 


  const request = new Request("http://127.0.0.1:8000/pipeline", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question: newMessage,
      retrieval_strategy: retrievalStrategies,
      index:openSearchIndices,
      llm: llms,
      citation: String(citationActive)
    }),
  });

  const checkInput = () => {
    if (newMessage.trim() == "") {
      alert("Message can't be empty!");
      return
    }
    if(openSearchIndices == "" || retrievalStrategies == "" || llms == "" ){
      alert("Complete the Configuration!");
      return
    }
    handleSendMessage();
    
  };

  async function handleSendMessage() {
    console.log(newMessage);
    setMessages([...messages, { text: newMessage, type: "user" }]);
    setNewMessage("");
    try {
      const response = await fetch(request);
      const data = await response.json();
      console.log(data);

      if (response.status === 200) {
        setMessages((prevMessages: any) => [
          ...prevMessages,
          { text: data, type: "assistant" },
        ]);
      } else {
        console.log("Something went wrong");
      }
    } catch (error) {
      console.log(error);
    }
  }

  return (
    <><Box
      sx={{
        display: "flex",
        flexDirection: "column",
        height: "50%",
        width: "50%",
        position: "absolute",
        top: "50%",
        left: "45%",
        transform: "translate(-50%, -50%)",
        border: "1px solid gray",
        borderRadius: "10px",
        marginBottom: "20px"
      }}
    >
      <Box sx={{ overflow: "auto", flexGrow: 1 }}>
        <List>
          {messages.map((message: any, index: any) => (
            <ListItem
              key={index}
              sx={{
                justifyContent: message.type === "user" ? "flex-end" : "flex-start",
              }}
            >
              <ListItemText
                sx={{
                  textAlign: message.type === "user" ? "right" : "left",
                }}
                primary={<Typography
                  variant="body1"
                  sx={{
                    backgroundColor: message.type === "user" ? "lightblue" : "grey",
                    padding: "5px",
                    borderRadius: "10px",
                    display: "inline-block",
                  }}
                >
                  {message.text}
                </Typography>} />
            </ListItem>
          ))}
        </List>
      </Box>
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          padding: 1,
          borderTop: "1px solid gray",
        }}
      >
        <TextField
          value={newMessage}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
            setNewMessage(e.target.value);
          } }
          variant="outlined"
          placeholder="Write a message"
          sx={{
            flexGrow: 1,
            marginRight: 1,
            borderColor: "primary.main",
            borderWidth: 2,
            borderRadius: "5px",
          }}
          inputProps={{ maxLength: MAX_CHARACTERS }} />
        <Typography variant="body2">
          {MAX_CHARACTERS - newMessage.length}/4000
        </Typography>
        <Button onClick={checkInput} variant="contained">
          Send
        </Button>
      </Box>
      
    </Box>
    <Box sx={{
              display: "flex",
              flexDirection: "column",
              height: "50%",
              width: "8%",
              position: "absolute",
              top: "100%",
              left: "24%",
              transform: "translate(-50%, -50%)",
              marginTop: "10px"
            }}
        >
        <button onClick = {AdvancedMode}>
          Advanced Mode: {showBox ? 'On' : 'Off'}
        </button>
      </Box>
    {showBox && (
    <Box sx={{
        display: "flex",
        flexDirection: "column",
        height: "50%",
        width: "20%",
        position: "absolute",
        top: "50%",
        left: "80%",
        transform: "translate(-50%, -50%)",
        border: "1px solid gray",
        borderRadius: "10px",
        marginLeft: "10px"
      }}>
      
      <div className="dropdown">
        <select id="dropdown1" value={retrievalStrategies} onChange={handleDropdownChange_retrieval}>
          <option value="">Retrieval Strategy</option>
          {retrievalStrategies_list.map(item => (
            <option value={item}>
              {item}
            </option>
          ))}
        </select>
      </div>

      <div className="dropdown">
        <select id="dropdown2" value={openSearchIndices} onChange={handleDropdownChange_index}disabled={disableSelectIndex}>
        
        <option value="">Select an Index</option>
        {openSearchIndices_list.map(item => (
            <option value={item}>
              {item}
            </option>
          ))}
        </select>
      </div>

      <div className="dropdown">
        <select id="dropdown3" value={llms} onChange={handleDropDownChange_llm}>
        <option value="">Select a LLM</option>
        {llms_list.map(item => (
            <option value={item}>
              {item}
            </option>
          ))}
        </select>
      </div>
      <div>
      <FormControlLabel sx={{
          paddingLeft: "15px"
        }}
        control={<Switch checked={citationActive} onChange={() => {
          setCitationActive(!citationActive)
          console.log("Citation Mode: ",citationActive)
        }} />}
        label= "Citation Mode"
      />
    </div>
    <Box sx={{ paddingLeft: "5px" }}>
      <CustomWidthTooltip   arrow placement="right-start" title="Please Configure your pipeline. The suggested default Configration is Hybrid Search with Voyage-2-large 
      and GPT 3.5 Turbo 0125 for Generation">
        <IconButton>
          <HelpOutlineIcon />
        </IconButton>
      </CustomWidthTooltip >
    </Box>
    


  
      </Box>)}

      
      </>
  );
};

export default ChatComponent;
