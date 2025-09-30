import { useState, useEffect } from 'react';
import styled from 'styled-components';

const StyledTarefa = styled.li`
  background: ${(props) =>
    props.concluida ? props.theme.colors.secondary : props.theme.colors.background};
  color: ${(props) =>
    props.concluida ? '#155724' : props.theme.colors.text};
  margin: ${({ theme }) => theme.spacings.small} 0;
  padding: ${({ theme }) => theme.spacings.medium};
  border-radius: 5px;
  font-size: ${({ theme }) => theme.fontSizes.medium};
  text-decoration: ${(props) => (props.concluida ? 'line-through' : 'none')};
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const ConcluirButton = styled.button`
  background: ${({ theme }) => theme.colors.buttonBackground};
  color: ${({ theme }) => theme.colors.buttonText};
  border: none;
  padding: 5px 10px;
  border-radius: 3px;
  cursor: pointer;

  &:hover {
    background: #218838;
  }
`;

function Tarefa({
  nome,
  concluida,
  descricao,
  onConcluir,
  onDelete,
  onEditar,
  onSalvar,
  isEditando,
}) {
  const [nomeEditado, setNomeEditado] = useState(nome);
  const [descricaoEditada, setDescricaoEditada] = useState(descricao);
  const [mostrarOpcoes, setMostrarOpcoes] = useState(false);

  useEffect(() => {
    if (isEditando) {
      setNomeEditado(nome);
      setDescricaoEditada(descricao);
    }
  }, [isEditando, nome, descricao]);

  if (isEditando) {
    return (
      <li>
        <input
          type="text"
          value={nomeEditado}
          onChange={(e) => setNomeEditado(e.target.value)}
        />
        <input
          type="text"
          value={descricaoEditada}
          onChange={(e) => setDescricaoEditada(e.target.value)}
        />
        <button onClick={() => onSalvar(nomeEditado, descricaoEditada)}>
          Salvar
        </button>
        <button onClick={() => onEditar(null)}>Cancelar</button>
      </li>
    );
  }

  return (
    <StyledTarefa as="li" concluida={concluida}>
      <span>{nome} - </span>
      <span>{descricao}</span>
      <ConcluirButton onClick={() => setMostrarOpcoes(!mostrarOpcoes)}>☰</ConcluirButton>

      {mostrarOpcoes && (
        <div className="opcoes">
          <button onClick={onConcluir}>Concluir</button>
          <button onClick={onEditar}>Editar</button>
          <button onClick={onDelete}>❌</button>
        </div>
      )}
    </StyledTarefa>
  );
}

export default Tarefa;
