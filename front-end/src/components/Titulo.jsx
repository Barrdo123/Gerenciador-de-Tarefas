import styled from 'styled-components';
const StyledTitulo = styled.h2`
 font-size: ${({ theme }) => theme.fontSizes.large};
 color: ${({ theme }) => theme.colors.text};
 margin-bottom: ${({ theme }) => theme.spacings.large};
`;
function Titulo({ texto }) {
    return (
        <StyledTitulo>{texto}</StyledTitulo>
    );
}
export default Titulo;
