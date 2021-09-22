import PropTypes from 'prop-types';
import { unicodeSymbols } from '../constants/constants';

const Unicode = ({ symbol }) => unicodeSymbols[symbol];

Unicode.propTypes = {
  symbol: PropTypes.string,
};

Unicode.defaultProps = {
  symbol: '',
};

export default Unicode;
