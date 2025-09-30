const tarefaRepository = require('../repositories/tarefaRepository');
const TarefaRepository = require('../repositories/tarefaRepository');

class TarefaController {
    async getAllTarefas(req, res) {
        try {
            const tarefas = await TarefaRepository.getAllTarefas();
            res.json(tarefas);

        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async createTarefa(req, res) {
        const { titulo, descricao, concluida } = req.body;
        try {

            const novaTarefa = await TarefaRepository.createTarefa({ titulo, descricao, concluida });
            res.status(201).json(novaTarefa);

        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async getTarefaById(req, res) {
        const { id } = req.params;
        
        if (id <= 0) {
            return res.status(400).json({ error: 'ID inválido' });
        }
        try {
            const tarefaById = await TarefaRepository.getTarefaById(id)

            if (!tarefaById) {
                return res.status(404).json({ error: 'Tarefa não encontrada' });
            }

            return res.status(200   ).json(tarefaById);


        } catch (error) {
            return res.status(500).json({ error: error.message });
        }

    }

    async updateTarefa(req, res){
        const {id} = req.params;
        const dados = req.body;

        if(id <= 0 || !dados || Object.keys(dados).length === 0){
            return res.status(400).json({ error: 'ID inválido ou dados ausentes!' });
        }
        try{
            const updateTarefa = await TarefaRepository.updateTarefa(id, dados)

            if(!updateTarefa){
                return res.status(404).json({error:'Tarefa não encontrada'})
            }

            return res.status(200).json(updateTarefa)

        } catch (error){
            return res.status(500).json({error:error.message})
        }
    }

    async deleteTarefas(req, res){
        const {id} = req.params

        if (id <= 0) {
            return res.status(400).json({ error: 'ID inválido' });
        }

        try{
            const deleteTarefa = await TarefaRepository.deleteTarefa(id)
            return res.status(200).json(deleteTarefa)

        } catch (error){
            return res.status(500).json({error:error.message})
        }
    }
}




module.exports = new TarefaController();
