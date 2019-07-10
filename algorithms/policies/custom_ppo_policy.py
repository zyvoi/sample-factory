import tensorflow as tf

from ray.rllib.agents.ppo.ppo_policy import PPOTFPolicy, kl_and_loss_stats


def _mean_min_max(x, name):
    fetches = {
        f'{name}_mean': tf.reduce_mean(x),
        f'{name}_min': tf.reduce_min(x),
        f'{name}_max': tf.reduce_max(x),
    }
    return fetches


def stats(policy, batch_tensors):
    stats_fetches = kl_and_loss_stats(policy, batch_tensors)
    stats_fetches.update(_mean_min_max(policy.value_function, '_value_estimate'))
    stats_fetches.update(_mean_min_max(tf.reduce_mean(batch_tensors['value_targets']), '_returns'))
    stats_fetches.update(_mean_min_max(tf.reduce_mean(batch_tensors['rewards']), '_rewards'))
    stats_fetches.update(_mean_min_max(tf.reduce_mean(batch_tensors['advantages']), '_advantage'))
    return stats_fetches


# noinspection PyUnusedLocal
def grad_stats(policy, grads):
    return dict(
        grad_gnorm=tf.global_norm(grads),
    )


CustomPPOTFPolicy = PPOTFPolicy.with_updates(
    stats_fn=stats,
    grad_stats_fn=grad_stats,
)
