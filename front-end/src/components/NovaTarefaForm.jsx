import { useRef } from "react";

function NovaTarefaForm({ novaTarefa, descricao, setNovaTarefa, setDescricao, onAdicionar }) {
  const inputRef = useRef(null);

  const handleAdd = () => {
    onAdicionar();
    inputRef.current?.focus(); // volta o foco para o input de título
  };

  return (
    <div>
      <input
        ref={inputRef}
        type="text"
        value={novaTarefa}
        onKeyDown={(e) => e.key === "Enter" && handleAdd()}
        onChange={(e) => setNovaTarefa(e.target.value)}
        placeholder="Adicionar nova tarefa"
      />

      <input
        type="text"
        value={descricao}
        onChange={(e) => setDescricao(e.target.value)}
        placeholder="Descrição"
      />

      <button onClick={handleAdd}>Adicionar</button>
    </div>
  );
}

export default NovaTarefaForm;
