import CustomSearchBar from './CustomSearchBar';
import CustomTable from './CustomTable';
import Header from './Header';
import Footer from './Footer';

const FrontPage = ({data, setUserSearch}) => {

    return (
        <div>
            <Header/>
            <CustomSearchBar setUserSearch = {setUserSearch}/>    
            <CustomTable data={data}/>
            <Footer/>
        </div>
    )
}

export default FrontPage