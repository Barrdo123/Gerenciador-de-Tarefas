const express = require('express');
const tarefaController = require('../controllers/tarefaController');
const router = express.Router();


router.get('/', (req, res) => tarefaController.getAllTarefas(req, res));
router.post('/', (req, res) => tarefaController.createTarefa(req, res));
router.get('/:id', (req, res) => tarefaController.getTarefaById(req, res));
router.put('/:id', (req, res) => tarefaController.updateTarefa(req, res));
router.delete('/:id', (req, res) => tarefaController.deleteTarefas(req, res));


module.exports = router;