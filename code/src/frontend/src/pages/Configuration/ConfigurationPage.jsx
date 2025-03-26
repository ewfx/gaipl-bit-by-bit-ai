import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import './ConfigurationPage.css';
import Header from '../../components/Header/Header';
import { useSelector } from 'react-redux';
import { selectUser } from '../../features/user/userSlice';
import Loader from '../../components/Loader/Loader';

const ConfigurationPage = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const chatEndRef = useRef(null);
  const navigate = useNavigate();
  const [optionsShown, setOptionsShown] = useState(false);
  const [ciNumberEntered, setCiNumberEntered] = useState(false);
  const [ciNumber, setCiNumber] = useState('');
  const options = [
    'Health Check',
    'Bring up node',
    'Shut the node',
    'Last 24 hrs Grafana stats',
    'Alerts generated',
    'Related incidents or changes',
    'Dependencies',
    'Patching status',
    'Patching schedule',
    'Node Ownership',
    'CI Outage Check',
    'Something else!'
  ];

  const [isLoading, setIsLoading] = useState(false);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const user = useSelector(selectUser);
  const location = useLocation();

  useEffect(() => {

    if (user?.email == null && location.pathname !== "/"){
      window.alert("Please login to continue");
      navigate("/");
    }
    // First message
    setMessages([{ type: 'user', text: 'Configuration Items' }]);

    // Second message after a delay
    const timer = setTimeout(() => {
      setMessages(prev => [...prev, 
        { type: 'bot', text: `Hello ${user?.username}! To begin with, please enter your CI number in the chat.` }
      ]);
    }, 1000); // 1 second delay

    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Add this function to handle API calls
  const handleBotResponse = async (userMessage) => {
    setIsLoading(true); // Start loading
    try {
      const response = await fetch('http://127.0.0.1:5000/ci-agent', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
        withCredentials: true,
        body: JSON.stringify({ "user_prompt": userMessage })
      });
      const data = await response.json();
      // console.log(data);
      setIsLoading(false); // Stop loading after getting response
      return data?.data?.messages[data?.data?.messages?.length - 1]?.content;
    } catch (error) {
      console.error('Error:', error);
      setIsLoading(false); // Stop loading on error
      return "Sorry, I encountered an error processing your request.";
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;
    console.log(inputMessage);
    // Add user message
    setMessages(prev => [...prev, { type: 'user', text: inputMessage }]);
    const userMessage = inputMessage;
    setInputMessage('');

    // Reset textarea height
    const textarea = e.target.querySelector('.chat-input');
    if (textarea) {
        textarea.style.height = '40.4px';
    }

    // Only show options message the first time after CI number
    if (!ciNumberEntered) {
      setCiNumberEntered(true);
      setCiNumber(inputMessage)
      setTimeout(() => {
        setMessages(prev => [...prev, {
          type: 'bot',
          text: 'To give me more context about the action to perform, please select one of the below options -',
          options: options
        }]);
      }, 1000);
    } else {
      // Handle API call for user's custom message
      setTimeout(async () => {
        const botResponse = await handleBotResponse(userMessage);
        setMessages(prev => [...prev, {
          type: 'bot',
          text: botResponse,
          options: [] // Keep options visible but don't prompt for them
        }]);
      }, 1000);
    }
  };

  const renderMessages = () => {
    return (
      <>
        {messages.map((message, index) => {
          if (message.type === 'bot') {
            return (
              <div key={index} className={`message ${message.type}`}>
                <div className="message-avatar">
                  🤖
                </div>
                <div className='message-content-container'>
                  <div className="message-content">
                    {message.text}
                    {message.options && (
                      <div className="options-grid-container">
                        <div className="options-grid">
                          {message.options.map((option, idx) => (
                            <button 
                              key={idx} 
                              className="option-button"
                              onClick={async () => {
                                setMessages(prev => [...prev, 
                                  { type: 'user', text: option }
                                ]);
                                const botResponse = await handleBotResponse(`Please provide me ${option} for the CI number ${ciNumber}`);
                                setMessages(prev => [...prev, {
                                  type: 'bot',
                                  text: botResponse,
                                  options: []
                                }]);
                              }}
                            >
                              {option}
                            </button>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          }

          return (
            <div key={index} className={`message ${message.type}`}>
              <div className="message-avatar">
                {message.type === 'bot' ? '🤖' : user?.username.toUpperCase().charAt(0)}
              </div>
              <div className='message-content-container'>
                <div className="message-content">
                  {message.text}
                </div>
              </div>
            </div>
          );
        })}
        {/* Add loader after messages if loading */}
        {isLoading && (
          <div className="message bot">
            <div className="message-avatar">
              🤖
            </div>
            <div className="message-content-container">
              <div className="message-content">
                <Loader />
              </div>
            </div>
          </div>
        )}
      </>
    );
  };

  return (
    <div>
        <Header />
        <div className="chat-container">
            <div className="breadcrumb">
                <Link to="/" className="home-link" onClick= {async () => {
                  try {
                    const response = await fetch('http://127.0.0.1:5000/flush', {
                      method: 'POST',
                      headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                      },
                      withCredentials: true
                    });
                    const data = await response.json();
                    console.log(data);
                    return data;
                  } catch (error) {
                    console.error('Error:', error);
                    return "Sorry, I encountered an error processing your request.";
                  }
                }}>Home</Link>
                <span className="separator"> {'>'} </span>
                <span className="breadcrumb-text">Configuration Items</span>
            </div>

            <div className="chat-messages">
                {renderMessages()}
                <div ref={chatEndRef} />
            </div>

            <form onSubmit={handleSubmit} className="chat-input-form">
                <textarea
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    placeholder="Type your message here..."
                    className="chat-input"
                    rows="1"
                    onInput={(e) => {
                        e.target.style.height = 'auto';
                        e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px';
                    }}
                />
                <button type="submit" className="send-button">Send</button>
            </form>
        </div>
    </div>
  );
};

export default ConfigurationPage;