import React from 'react';
import axios from 'axios';

const SERVER_DOMAIN = 'http://localhost:5000'
const COMPANY_INFO_ENPOINT = `${SERVER_DOMAIN}/api/getCompanyInfo`
const COMPARE_PEERS_ENPOINT = `${SERVER_DOMAIN}/api/getComparePeers`

export const getCompanyInfo = () => axios.get(COMPANY_INFO_ENPOINT)
export const getComparePeers = () => axios.get(COMPARE_PEERS_ENPOINT)