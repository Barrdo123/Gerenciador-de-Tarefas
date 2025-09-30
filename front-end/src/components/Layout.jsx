import styled from 'styled-components';
const Container = styled.div`
    width: 100%;
    margin: 50px 50% 50px;
    padding: 20px;
    background: #e5e7d6ff;
    border-radius: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    text-align: center;
`;

function Layout({ children }) {
    return <Container>{children}</Container>;
}
export default Layout;