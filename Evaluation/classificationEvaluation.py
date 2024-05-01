import logging


def accuracy(num_tp, num_fn, num_fp, num_tn):
    """
     Accuracy is calculated as (TP + TN) / (TP + FP + FN + TN).
  """

    return float(num_tp + num_tn) / (num_tp + num_fp + num_fn + num_tn)


# -----------------------------------------------------------------------------

def precision(num_tp, num_fp):
    """

     Precision is calculated as TP / (TP + FP).

  """

    if num_fp + num_tp == 0:
        return 0.0
    return float(num_tp) / (num_tp + num_fp)


# -----------------------------------------------------------------------------

def recall(num_tp, num_fn):
    """
     Recall is calculated as TP / (TP + FN).
  """

    if num_fn + num_tp == 0:
        return 0.0
    return float(num_tp) / (num_tp + num_fn)


# -----------------------------------------------------------------------------

def f_measure(num_tp, num_fn, num_fp):
    """
    f measure is calculated as 2 * (precision * recall) / (precision + recall).

  """

    rec = recall(num_tp, num_fn)
    prec = precision(num_tp, num_fp)

    if prec + rec == 0.0:
        return 0.0

    return 2 * (prec * rec) / (prec + rec)


def classification_evaluation(db_context, m_utilites):
    num_tp, num_fp, num_fn, num_tn = db_context.get_classification_evaluation_data(
        m_utilites.get_number_of_matching_candidates_before_blocking())

    print('')

    logging.info('general linkage evaluation:')
    logging.info(f'TP: {num_tp}, FP: {num_fp}, FN: {num_fn}, TN: {num_tn}')
    logging.info('  Accuracy:    %.4f' % (accuracy(num_tp, num_fn, num_fp, num_tn)))
    logging.info('  Precision:   %.4f' % (precision(num_tp, num_fp)))
    logging.info('  Recall:      %.4f' % (recall(num_tp, num_fn)))
    logging.info('  F-score:     %.4f' % (f_measure(num_tp, num_fn, num_fp)))


def th_gw_classification_evaluation(data_alias, db_context, m_utilites):
    if data_alias == 'th':
        potential_matches = m_utilites.get_number_of_th_matching_candidates_before_blocking()
        dataset = 'Tommy Hilfiger'
    else:
        potential_matches = m_utilites.get_number_of_gw_matching_candidates_before_blocking()
        dataset = 'Gerry Weber'
    num_tp, num_fp, num_fn, num_tn = db_context.get_th_gw_classification_evaluation_data(potential_matches, data_alias)

    logging.info(f'{dataset} - Zalando linkage evaluation:')
    logging.info(f'TP: {num_tp}, FP: {num_fp}, FN: {num_fn}, TN: {num_tn}')
    logging.info('  Accuracy:    %.4f' % (accuracy(num_tp, num_fn, num_fp, num_tn)))
    logging.info('  Precision:   %.4f' % (precision(num_tp, num_fp)))
    logging.info('  Recall:      %.4f' % (recall(num_tp, num_fn)))
    logging.info('  F-score:     %.4f' % (f_measure(num_tp, num_fn, num_fp)))



