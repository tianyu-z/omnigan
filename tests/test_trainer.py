import sys

sys.path.append("..")

from omnigan.trainer import Trainer
from omnigan.utils import load_opts
from run import print_header

if __name__ == "__main__":
    opts = load_opts("../shared/defaults.yml")
    trainer = Trainer(opts, verbose=1)

    test_setup = True
    test_get_representation_loss = True
    test_get_translation_loss = True
    test_update_g = True

    if test_setup:
        print_header("test_setup")
        trainer.setup()

    if test_get_representation_loss:
        print_header("test_get_representation_loss")
        if not trainer.is_setup:
            trainer.setup()
        multi_batch_tuple = next(iter(trainer.train_loaders))
        domain_batch = {batch["domain"][0]: batch for batch in multi_batch_tuple}
        loss = trainer.get_representation_loss(domain_batch)
        print("Loss {}".format(loss.item()))

    if test_get_translation_loss:
        print_header("test_get_translation_loss")
        if not trainer.is_setup:
            trainer.setup()

        multi_batch_tuple = next(iter(trainer.train_loaders))
        domain_batch = {batch["domain"][0]: batch for batch in multi_batch_tuple}
        loss = trainer.get_translation_loss(domain_batch)
        print("Loss {}".format(loss.item()))

    if test_update_g:
        print_header("test_update_g")
        if not trainer.is_setup:
            trainer.setup()

        trainer.verbose = 0

        multi_batch_tuple = next(iter(trainer.train_loaders))
        domain_batch = {batch["domain"][0]: batch for batch in multi_batch_tuple}

        # Using repr_tr and step < repr_step and step % 2 == 0
        trainer.opts.train.representational_training = True
        trainer.opts.train.representation_steps = 100
        trainer.logger.step = 0

        trainer.update_g(domain_batch)

        # Using repr_tr and step < repr_step and step % 2 == 1
        trainer.opts.train.representational_training = True
        trainer.opts.train.representation_steps = 100
        trainer.logger.step = 1

        trainer.update_g(domain_batch)

        # Using repr_tr and step > repr_step
        trainer.opts.train.representational_training = True
        trainer.opts.train.representation_steps = 100
        trainer.logger.step = 200

        trainer.update_g(domain_batch)

        # Not Using repr_tr and step < repr_step and step % 2 == 0
        trainer.opts.train.representational_training = False
        trainer.opts.train.representation_steps = 100
        trainer.logger.step = 200

        trainer.update_g(domain_batch)

        # Not Using repr_tr and step > repr_step and step % 2 == 1
        trainer.opts.train.representational_training = False
        trainer.opts.train.representation_steps = 100
        trainer.logger.step = 201

        trainer.update_g(domain_batch)
